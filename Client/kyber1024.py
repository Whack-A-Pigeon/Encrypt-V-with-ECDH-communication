import os
from hashlib import sha3_256, sha3_512, shake_128, shake_256
from polynomials import *
from modules import *
from ntt_helper import NTTHelperKyber
try:
    from aes256_ctr_drbg import AES256_CTR_DRBG
except ImportError as e:
    print("Error importing AES CTR DRBG. Have you tried installing requirements?")
    print(f"ImportError: {e}\n")
    print("Kyber will work perfectly fine with system randomness")

class Kyber:
    def __init__(self):
        self.n = 256
        self.k = 4
        self.q = 3329
        self.eta_1 = 2
        self.eta_2 = 2
        self.du = 11
        self.dv = 5
        
        self.R = PolynomialRing(self.q, self.n, ntt_helper=NTTHelperKyber)
        self.M = Module(self.R)
        
        self.drbg = None
        self.random_bytes = os.urandom
        
    def set_drbg_seed(self, seed):
        self.drbg = AES256_CTR_DRBG(seed)
        self.random_bytes = self.drbg.random_bytes

    def reseed_drbg(self, seed):
        if self.drbg is None:
            raise Warning(f"Cannot reseed DRBG without first initialising. Try using `set_drbg_seed`")
        else:
            self.drbg.reseed(seed)
        
    @staticmethod
    def _xof(bytes32, a, b, length):
        input_bytes = bytes32 + a + b
        if len(input_bytes) != 34:
            raise ValueError(f"Input bytes should be one 32 byte array and 2 single bytes.")
        return shake_128(input_bytes).digest(length)
        
    @staticmethod
    def _h(input_bytes):
        """
        H: B* -> B^32
        """
        return sha3_256(input_bytes).digest()
    
    @staticmethod  
    def _g(input_bytes):
        output = sha3_512(input_bytes).digest()
        return output[:32], output[32:]
    
    @staticmethod  
    def _prf(s, b, length):
        input_bytes = s + b
        if len(input_bytes) != 33:
            raise ValueError(f"Input bytes should be one 32 byte array and one single byte.")
        return shake_256(input_bytes).digest(length)
    
    @staticmethod
    def _kdf(input_bytes, length):
        return shake_256(input_bytes).digest(length)
    
    def _generate_error_vector(self, sigma, eta, N, is_ntt=False):
        elements = []
        for i in range(self.k):
            input_bytes = self._prf(sigma,  bytes([N]), 64*eta)
            poly = self.R.cbd(input_bytes, eta, is_ntt=is_ntt)
            elements.append(poly)
            N = N + 1
        v = self.M(elements).transpose()
        return v, N
        
    def _generate_matrix_from_seed(self, rho, transpose=False, is_ntt=False):
        A = []
        for i in range(self.k):
            row = []
            for j in range(self.k):
                if transpose:
                    input_bytes = self._xof(rho, bytes([i]), bytes([j]), 3*self.R.n)
                else:
                    input_bytes = self._xof(rho, bytes([j]), bytes([i]), 3*self.R.n)
                aij = self.R.parse(input_bytes, is_ntt=is_ntt)
                row.append(aij)
            A.append(row)
        return self.M(A)
        
    def _cpapke_keygen(self):
        # Generate random value, hash and split
        d = self.random_bytes(32)
        rho, sigma = self._g(d)
        # Set counter for PRF
        N = 0
        
        # Generate the matrix A ∈ R^kxk
        A = self._generate_matrix_from_seed(rho, is_ntt=True)
        
        # Generate the error vector s ∈ R^k
        s, N = self._generate_error_vector(sigma, self.eta_1, N)
        s.to_ntt()
        
        # Generate the error vector e ∈ R^k
        e, N = self._generate_error_vector(sigma, self.eta_1, N)
        e.to_ntt() 
                           
        # Construct the public key
        t = (A @ s).to_montgomery() + e
        
        # Reduce vectors mod^+ q
        t.reduce_coefficents()
        s.reduce_coefficents()
        
        # Encode elements to bytes and return
        pk = t.encode(l=12) + rho
        sk = s.encode(l=12)
        return pk, sk
        
    def _cpapke_enc(self, pk, m, coins):
        N = 0
        rho = pk[-32:]
        
        tt = self.M.decode(pk, 1, self.k, l=12, is_ntt=True)        
        
        # Encode message as polynomial
        m_poly = self.R.decode(m, l=1).decompress(1)
        
        # Generate the matrix A^T ∈ R^(kxk)
        At = self._generate_matrix_from_seed(rho, transpose=True, is_ntt=True)
        
        # Generate the error vector r ∈ R^k
        r, N = self._generate_error_vector(coins, self.eta_1, N)
        r.to_ntt()
        
        # Generate the error vector e1 ∈ R^k
        e1, N = self._generate_error_vector(coins, self.eta_2, N)
        
        # Generate the error polynomial e2 ∈ R
        input_bytes = self._prf(coins,  bytes([N]), 64*self.eta_2)
        e2 = self.R.cbd(input_bytes, self.eta_2)
        
        # Module/Polynomial arithmetic 
        u = (At @ r).from_ntt() + e1
        v = (tt @ r)[0][0].from_ntt()
        v = v + e2 + m_poly
        
        # Ciphertext to bytes
        c1 = u.compress(self.du).encode(l=self.du)
        c2 = v.compress(self.dv).encode(l=self.dv)
        
        return c1 + c2
    
    def _cpapke_dec(self, sk, c):
        # Split ciphertext to vectors
        index = self.du * self.k * self.R.n // 8
        c2 = c[index:]
        
        # Recover the vector u and convert to NTT form
        u = self.M.decode(c, self.k, 1, l=self.du).decompress(self.du)
        u.to_ntt()
        
        # Recover the polynomial v
        v = self.R.decode(c2, l=self.dv).decompress(self.dv)
        
        # s_transpose (already in NTT form)
        st = self.M.decode(sk, 1, self.k, l=12, is_ntt=True)
        
        # Recover message as polynomial
        m = (st @ u)[0][0].from_ntt()
        m = v - m
        
        # Return message as bytes
        return m.compress(1).encode(l=1)
    
    def keygen(self):
        pk, _sk = self._cpapke_keygen()
        z = self.random_bytes(32)
        
        # sk = sk' || pk || H(pk) || z
        sk = _sk + pk + self._h(pk) + z
        return pk, sk
        
    def enc(self, pk, key_length=32):
        m = self.random_bytes(32)
        m_hash = self._h(m)
        Kbar, r = self._g(m_hash + self._h(pk))
        c = self._cpapke_enc(pk, m_hash, r)
        K = self._kdf(Kbar + self._h(c), key_length)
        return c, K

    def dec(self, c, sk, key_length=32):
        index = 12 * self.k * self.R.n // 8
        _sk =  sk[:index]
        pk = sk[index:-64]
        hpk = sk[-64:-32]
        z = sk[-32:]
        
        # Decrypt the ciphertext
        _m = self._cpapke_dec(_sk, c)
        
        # Decapsulation
        _Kbar, _r = self._g(_m + hpk)
        _c = self._cpapke_enc(pk, _m, _r)
        
        # if decapsulation was successful return K
        if c == _c:
            return self._kdf(_Kbar + self._h(c), key_length)
        # Decapsulation failed... return random value
        return self._kdf(z + self._h(c), key_length)

