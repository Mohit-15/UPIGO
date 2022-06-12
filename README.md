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

    PATCH: https://127.0.0.1:8000/api/user/editUserDetails/
    headers: {"Bearer": <authentication_token>}
This end point is used to edit the existing user details, and returns the updated UserDetail object in the response.


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

    GET: https://127.0.0.1:8000/api/user/generateOTP/
    headers: {"Bearer": <authentication_token>}
This request will fetch the user registered mobile number and sends an OTP via SMS, and also put the same OTP in the ***"VERIFICATION_OTP"*** header. For sending SMS, I'm using **Twilio APIs**.


