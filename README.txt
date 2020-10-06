Document

on Django
Customer Data
    - customerID
        primary key, auto increment
    - email
    - phoneNumber (phone_number)
    - username
    - password
        hashed
    - createdAt (date_joined)
    - updatedAt (updated_at)

on Java
User Registration Verification
        -> ketika user registrasi, dibuat model usernya, minta api java buatin OTPnya, kasih lagi ke user by email
        -> langsung redirect ke form masukin otp, tinggal passing form datanya
        -> hit form + otp ke api java, validasi bener atau ngga, update database
    - otpID
        primary key, auto increment
    - customerID
        foreign key, to Customer Data
    - otpNumber
    - email
    - createdAt
    - validUntil
    - status
        udah diverifikasi sama usernya atau belom

batal
Temporary OTP Table
    - username
    - email
    - otpNumber
    
    - requestHeader
    - requestBody

    script checks this table to send email, then deletes Temporary otp, updates status

Transaction Log
    - transactionID
    - customerID
    - tierID
    - username
    - discounted
    - transactionAmmount
    - discountedAmmount
    - transactionTime

on Java
Transaction Tier
    - tierID
        primary key, auto increment
    - minimumTransaction
    - maximumTransaction
    - probability
    - discount

Log
API Log
    - logID
    - responseID
    - ip
    - requestType
        Transaction or Login or OTP
            -> when user Login, hit Java API to store APILog on Login
            -> Transaction is hit by Ajax
    - requestHeader
    - requestBody
    - responseHeader
    - responseBody
    - status
    - statusDetails
    - timeRequested
    - timeResponded
    - elapsedTime

user management
    -> roles
    -> permission
    -> CRUD

    - admin
        -> CRUD
    - dashboard doang
        -> grafik
    - yang bisa ngehit apinya
        -> cek summary transaksi
            - detailed
            - summary

dashboard
    -> grafik
        - hit apinya berapa kali, per jamnya berapa
        - pertumbuhan otp
        - gagal suksesnya

smtp
    queueing
        -> Advanced (Message Broker)
            - RabitMQ
            - apache kafka
        -> basic
            -> using database and trigger