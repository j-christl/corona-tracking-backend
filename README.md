# corona-tracking-backend
Backend of the Corona Tracking App, developed in the context of the #WirVsVirus Hackathon by the german government. See https://wirvsvirushackathon.org/

# Dependencies
- Python 3.7
- websockets
- psycopg2-binary
- pyjwt
- boto3

# Setup
- To install all packages, run "pip3 install -r requirements.txt"

# Starting the server
- Enter "python3 server.py" in the terminal

# REST API Documentation
- Content-Type must be application/json
- All responses are in the following format:
```
{
    "success": True/False,
    "message": "Contains message if something went wrong",
    "payload": {
        // request payload here
    }
}
```
## Register User
```
POST /register
```

**Response payload:**
```
{
  "userId": // user ID here
  "jwt": // JSON Web Token here
}
```

## Upload tracking data
```
POST /track
```

**Parameters:**

Name | Type | Description
--- | :---: | ---
jwt | `object` | JSON Web Token

**Request body:**
```
{
  "contacts": [
    [
      OTHER_USER_ID,
      TIMESTAMP
    ],
    ...
  ],
  "positions": [
    [
      TIMESTAMP,
      LONGITUDE,
      LATITUDE
    ],
    ...
  ]
}
```

## Update user status
```
PATCH /userstatus
```

**Parameters:**

Name | Type | Description
--- | :---: | ---
jwt | `object` | JSON Web Token
status | `string` | User health status; Can be HEALTHY or INFECTED

## Get user status
```
GET /userstatus
```

**Parameters:**

Name | Type | Description
--- | :---: | ---
jwt | `object` | JSON Web Token

**Response payload:**
```
{
  "status": // user status here
}
```

## Upload Personal Data
```
POST /infected
```

**Parameters:**

Name | Type | Description
--- | :---: | ---
jwt | `object` | JSON Web Token
firstname | `string` | First name
lastname | `string` | Last name
phonenumber | `string` | Phone number
