# ENCRYPTI-V

### This is follow up on another repository of [Encrypti-V with RSA Communication](https://github.com/Whack-A-Pigeon/Encrypt-V-with-RSA-communication)

## About
Encrypti V is a file encryption and decryption tool designed to provide a secure way to protect your files. This README provides comprehensive instructions on setting up the tool, configuring the database, and using Python Version. Additionally, it includes information on the client-server version utilizing ECDHE+Kyber for communication.
## Features

- User registration and login
- Secure file encryption using AES-GCM
- File decryption with the correct encryption key
- Option to change the file name during encryption
- Option to save encrypted files in a different location
- Strong password enforcement
- Secure storage of encryption keys in a database

## Database Setup

### Prerequisites

- MySQL Server installed on your system.

### Steps

1. **Create Database:**

    ```sql
    CREATE DATABASE encryptiv_db;
    ```

2. **Use the Database:**

    ```sql
    USE encryptiv_db;
    ```

3. **Create Users Table:**

    ```sql
    CREATE TABLE users (
        user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(64) NOT NULL
    );
    ```

4. **Create Files Table:**

    ```sql
    CREATE TABLE files (
        user_id INT NOT NULL,
        file_id BINARY(32) NOT NULL,
        file_name VARCHAR(255) NOT NULL,
        encryption_key BINARY(32) NOT NULL,
        iv BINARY(16),
        PRIMARY KEY (file_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ```

5. **Summary:**

   - Database Name: `encryptiv_db`
   - Tables:
     - `users`
     - `files`

## Python Version

### Setup

To set up the Python version of Encrypti V, follow these steps:

#### Database Configuration

1. Make sure you have a MySQL database server set up and running.
2. Create a database named `encryptiv_db` in your MySQL server.
3. Update the database connection details in the `server.py` script.

```python
connection = pymysql.connect(host="localhost", user="your_username", password="your_password", database="encryptiv_db")
```

#### Required Modules

You need to install the following Python modules using `pip`:

- `pymysql`
- `PyQt6`
- `pycryptodome`
- `cryptography`

You can install these modules by running the following commands:

```bash
pip install pymysql
pip install PyQt6
pip install pycryptodome
pip install cryptography
```

#### How to Use

1. Run the `server.py` script on the server.

```bash
python server.py
```

2. Run the `client.py` script on the client.

```bash
python client.py
```

3. Follow the prompts to register/login and perform file encryption and decryption.

## Acknowledgements

- This project was developed using the Python programming language for the Python version and Java for the Java version.

- Encryption is performed using the Python version with the [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html) library and the Java version using Java's built-in encryption capabilities.

- The client-server version was implemented with the help of Python's socket programming.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
