## **UPI-GO Documentation**
<img src="https://i.imgur.com/LJl3pB2.jpg%29" alt="Unified Payment Interface" width="400"/>

This is a **Django REST** based **API** documentation of the whole ***UPI end-to-end cycle*** from user registration to email & mobile verification to create UPI ID to setting password to make a successful transaction. 
In this project, I've divided the whole project into three sub-parts. 
	

 1. User Account Application
 2. UPI IDs Application
 3. Transaction Application

As the name implies, User Account application handles all the user registration, Authentication, verification, etc. UPI IDs Application handles the operations related to UPI like creation, change password, activate/deactivate UPI ID etc. Same as Transaction Application handles the operations related to transaction and make our database consistent.

## User Accounts Application
The base url for user APIs starts with

    https://127.0.0.1:8000/api/user
    
In this application, we have used ***Token Authentication***, in which whenever a existing user logins with the correct credentials, then a JWT Token is created, which can be used to authorize the user request.

These are the operations which I have added to the User Account Application.

> - **createUser**
> - **loginUser**
> - **logoutUser**
> - **verifyMobileNumber**
> - **generateOTP**
> - **addUserDetails**
>  - **editUserDetails**
> - **showUserDetails**
> - **addMoneyToWallet**

### Create User API

    POST: https://127.0.0.1:8000/api/user/createUser/
    body: 
    {
	    "email": "<valid_email_address>",
	    "name": "<name>",
	    "mobile_no": "<valid_mobile_number>",
	    "password1": "<password>",
	    "password2": "<confirm_password>"
    }
    
I've taken Mobile Number as the username for authentication. When the user creation is successful, a user account object will be created in the database, and a email verification mail will be automatically sent to the user registered email, which contains the email verification link.

### Login User API

    POST: https://127.0.0.1:8000/api/user/loginUser/
    body: 
    {
	    "username": <mobile_no>,
	    "password": ""
    }
When the user logins with correct credentials, a response will be generated with a 200 status code, and a authentication token.

    {
	    "token": "932dfsfsdfisdf2023470dxfdfisdifdf"
    }
Whenever a user needs to make a request which needs authentication, then user can paste this token in the ***AUTHENTICATION HEADER***.

### Logout User API

    GET: https://127.0.0.1:8000/api/user/logoutUser/
    headers: {"bearer": <authentication_token>}
    
This endpoint will delete the **AUTHENTICATION TOKEN** object from the database, and logs out the user from the session. Whenever the same user logins, a new **TOKEN** will be generated and a new object is created in the TOKENS model.

### Add User Details API

    POST: https://127.0.0.1:8000/api/user/addUserDetails/
    headers: {"bearer": <authentication_token>}
    body: 
    {
	    "age": "<integer>",
	    "gender": "<Male/Female>",
	    "date_of_birth": "<YYYY-MM-DD>",
	    "address": "<your_address>",
	    "aadhar_number": "<aadhar_number>",
	    "pan_card": "<pan_card_number>"
    }
    
This API will create a **UserDetail** object in the database with logged in user as the user, and return all the details in the response with a **201** Created status code.

### Edit User Details API

    PATCH: https://127.0.0.1:8000/api/user/editUserDetails/
    headers: {"Bearer": <authentication_token>}
    
This end point is used to edit the existing user details, and returns the updated UserDetail object in the response.

### Show User Details API

    GET: https://127.0.0.1:8000/api/user/showUserDetails/
    headers: {"Bearer": <authentication_token>}
    Response: 
    {
	    "user": {
	        "email": "xxxxxxxxx@gmail.com",
	        "name": "Mohit Gupta",
	        "mobile_no": "xxxxxxxxxx"
	    },
	    "age": 22,
	    "gender": "Male",
	    "date_of_birth": "2000-04-15",
	    "address": "xxxx, xxxx xxxx xxxx.",
	    "aadhar_number": null,
	    "pan_card": null,
	    "account_balance": 530
    }

### Add Money to Account Wallet API

    POST: https://127.0.0.1:8000/api/user/addMoneyToWallet/
    headers: {"Bearer": <authentication_token>}
    body: 
    {
	    "amount": <Integer_value>
    }

> For now, I've taking the amount value from the form, but in future I'm
> planning to integrate **Paytm/Razorpay** gateway for adding the money
> to wallet.

This request will add the money to the respective **userDetail** object for making the transactions.

### Generate OTP for Registered Mobile number verification API

    GET: https://127.0.0.1:8000/api/user/generateOTP/
    headers: {"Bearer": <authentication_token>}
    
This request will fetch the user registered mobile number and sends an OTP via SMS, and also put the same OTP in the ***"VERIFICATION_OTP"*** header. For sending SMS, I'm using **Twilio APIs**.

### Verify Mobile Number API

    POST: http://127.0.0.1:8000/api/user/verifyMobileNumber/
    headers: {"Bearer": <authentication_token>}
    body: 
    {
	    "otp": <enter_otp_send_via_sms>
    }
    
This request will compare the OTPs in the **"VERIFICATION_OTP"** and the request body. If the OTPs match it will make the is_active boolean field **"TRUE"**, else return the error.

## Transactions Application
The base url for user APIs starts with

    https://127.0.0.1:8000/api/user/transactions/
    
This application handles Endpoints related to the transactions. These are the operations which I have added to the Transaction Application.

> * viewTransactions
> * makeTransaction
> * debitHistory
> * creditHistory

### View All Transactions API

    GET: https://127.0.0.1:8000/api/user/transactions/viewTransactions/
    headers: {"Bearer": <authentication_token>}
    Response Body: 
    [
	    {
	        "user": {
	            "email": "xxxxxxxx@gmail.com",
	            "name": "Mohit Gupta",
	            "mobile_no": "xxxxxxxxx"
	        },
	        "transaction_id": "8c646a2c-f930-4420-9c58-7a9d6e52e754",
	        "transfer_to": "xxxxxxxxxxx@upigo",
	        "received_from": null,
	        "amount": "-10",
	        "not_pending": true,
	        "is_credit": false,
	        "done_on": "2022-06-09T18:39:01.019706+05:30"
	    },
	    {
	        "user": {
	            "email": "xxxxxxxxx@gmail.com",
	            "name": "Mohit Gupta",
	            "mobile_no": "xxxxxxxxx"
	        },
	        "transaction_id": "7ec4167e-41dc-494c-9132-33e540145214",
	        "transfer_to": null,
	        "received_from": "xxxxxxxxxxx@upigo",
	        "amount": "+20",
	        "not_pending": true,
	        "is_credit": true,
	        "done_on": "2022-06-09T18:56:21.314813+05:30"
	    }
	]
	
The response body contains an **ARRAY** of transactions. The response body clearly shows which is a debit transaction and which is a credit transaction.  Whenever the logged in user receives money from someone, the is_credit field becomes TRUE, and the received from field will be field with the receiver's UPI Id. 
If it is the debit transaction, the amount will have the prefix **"-"**, and the transfer_to field will be filled.

### Make Transaction API

    POST: http://127.0.0.1:8000/api/user/transactions/makeTransaction/
    headers: {"Bearer": <authentication_token>}
    body: 
    {
		"transfer_to": "xxxxxxxxxxx@upigo",
		"amount": 10,
		"password": "xxxxxx"
	}
	
This endpoint requires three values, the upi_id of receiver, amount, and the UPI password. After successful transaction, the response body will look like this: 

> VALIDATION CHECKS BEFORE MAKING ANY TRANSACTION
> * For Making a transaction, user first needs to verify its mobile number, then only the user can successfully make any transaction.
> * Receiver's UPI ID should exist and active.
> * User wallet balance should not be zero.
> * Checks entered UPI PIN is correct or not.

    {
	    "transaction_id": "2343b7f7-e0bf-4b61-b51b-1f33ca7db132",
	    "transfer_to": "xxxxxxxxxxx@upigo",
	    "received_from": null,
	    "amount": "-10",
	    "is_credit": false,
	    "not_pending": true,
	    "done_on": "2022-06-12T20:23:27.187501+05:30",
	    "user": 1
	}
	
After successful transaction, the SMS will also be sent to the registered mobile numbers of the sender, and the receiver. The SMS will look like this: 

> Hello Mohit Gupta, Rs. 10 has been debited from your account to xxxxxxxxxxx@upigo.
> 
> The transaction id for this transaction is : 2343b7f7-e0bf-4b61-b51b-1f33ca7db132.
> 
> Thank you for using UPI GO.

### Debit History API

    GET: http://127.0.0.1:8000/api/user/transactions/debitHistory/
    headers: {"Bearer": <authentication_token>}
    
This endpoint will return an **ARRAY** of transactions, which include all the debited transactions from the User's Account.

### Credit History API

    GET: http://127.0.0.1:8000/api/user/transactions/creditHistory/
    headers: {"Bearer": <authentication_token>}
    
This endpoint will return an **ARRAY** of transactions, which include all the credited transactions to the User's Account.

## UPI Application

The base url for user APIs starts with

    https://127.0.0.1:8000/api/user/upi

> For now, I've made **One-to-One** Relation with the UPI object and the USER account. Means for one user, only one UPI ID is created.

This application handles Endpoints related to the UPI. These are the operations which I have added to the UPI Application.

> * createUpi
> * changeUpiID
> * changeUpiPin
> * deactivateUpi
> * showUpiDetails
> * reactivateUPI
> * scanQRCode

### Create UPI ID

    POST: http://127.0.0.1:8000/api/user/upi/createUpi/
    headers: {"Bearer": <authentication_token>}
    body: 
    {
	    "set_default": <0/1>,
	    "upi_id": "<custom_upi_ID>",
	    "pin1": "<upi_pin>",
	    "pin2": "<confirm_upi_pin>"
	}
    
In this API, I've provided two options for the users to choose their UPI ID. They can either set the default UPI ID i.e. "mobile_no@upigo" or the custom upi ID of their choice only by setting the **"set_default"** field with **0 or 1**.

> I've set one Validation for creating the UPI ID.
> * User first needs to verify their mobile number to create the UPI ID.

After successful creation of **UPI** object, an **QRCode** will also be created, which stores the **ENCODED UPI ID**. This QRCode can be used to make payments through scanning the code. 

<img src="https://i.imgur.com/OJjYIbW.png" alt="Example QR Code" width="400"/>

### Change UPI PIN API

    PATCH: http://127.0.0.1:8000/api/user/upi/changeUpiPin/
    headers: {"Bearer": <authentication_token>}
    body: 
    {
	    "pin1": "<upi_pin>",
	    "pin2": "<confirm_upi_pin>"
	}
	
This endpoint will take two fields **PIN1** and **PIN2**. This will change the password of the UPI ID associated with the logged in user account.

### Change UPI ID API

    PATCH: http://127.0.0.1:8000/api/user/upi/changeUpiID/
    headers: {"Bearer": <authentication_token>}
    body: 
    {
	    "upi_id": "<new_upi_id>",
	    "password": "<upi_pin>"
	}
	
This endpoint will change the **UPI ID** associated with the logged in user account, also creates a new encrypted **QR code** for the new UPI ID.

### Show UPI Details API

    GET: http://127.0.0.1:8000/api/user/upi/showUpiDetails/
    headers: {"Bearer": <authentication_token>}
    
This API will show the details of the Logged In user's UPI Details like this:

    [
	    {
		    "username": {
			    "email": "xxxxxxxxxxx@gmail.com",
			    "name": "Mohit Gupta",
			    "mobile_no": "xxxxxxxxxxx"
		    },
		    "upi_id": "xxxxxxxxxxx@upigo",
		    "created_at": "2022-06-08T22:30:16.185558+05:30",
		    "updated_at": "2022-06-12T22:28:25.667376+05:30",
		    "scan_code": "/media/upi/qr_codes/qrcode-xxxxxxxxxxx.png",
		    "is_active": true
	    }
	]

### Scan QR Code API

    POST: http://127.0.0.1:8000/api/user/upi/scanQRCode/
    headers: {"Bearer": <authentication_token>}
    body: 
    {
	    "qr_code": "<qr_code>"
    }
    
This API will fetch the text written in the QRCode, decodes it and find the matching UPI object from the Database, and returns the details, else returns the error saying **"No UPI Details found"** with **404** status code.
The encoded text in the QR Code will look like this:

> hkgfmiSk9-yzVjM_d2cFJkkbat9MarPPZCzWaxm_i8gLZOSOHhUKZvezH3e1s8M8bisllOXIG-ZkeH7viEWUIKkcA@upigo

Which is then decoded and converted into ***xxxxxxxxxx@upigo***.  For encoding & decoding, I've used ***Symmetric Key Cryptography***.

### Deactivate UPI Object API

    GET: http://127.0.0.1:8000/api/user/upi/deactivateUPI/
    headers: {"Bearer": <authentication_token>}
    
This API call makes the **is_active** field to **FALSE**, and restrict the UPI ID to make any transaction.

### Reactivate UPI Object API

    GET: http://127.0.0.1:8000/api/user/upi/reactivateUPI/
    headers: {"Bearer": <authentication_token>}
    
This API call makes the **is_active** field to **TRUE**, and allow the UPI ID to make any transaction.

<hr/>

> This project is my attempt to implement the entire UPI cycle. This repository may include several problems. Please submit a **pull request**. I'd want to make fresh contributions to assist make this project a huge success and a valuable resource for people interested in learning about FinTech.
> 
> Please do like if this repository somehow helped you :)
