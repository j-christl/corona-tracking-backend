# corona-tracking-backend
Backend of the Corona Tracking App, developed in the context of the #WirVsVirus Hackathon by the german government. See https://wirvsvirushackathon.org/

# Dependencies
- Python 3.7
- websockets
- psycopg2-binary
- pyjwt

# Setup
- To install all packages, run "pip3 install -r requirements.txt"

# Starting the server
- Enter "python3 server.py" in the terminal

# REST API Documentation
- Content-Type must be application/json
- Use Unix Timestamps
- All responses are in the following format:
```
{
    "success": True/False,
    "messages": "Contains message if something went wrong"
    "payload": {
        // request payload here
    }
}
```
## Test
```
GET /test
```
Just for testing

**Parameters:**

Name | Type | Description
--- | :---: | ---
jwt | `object` | JSON Web Token

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
      TIMESTAMP,
      USER_ID_0,
      USER_ID_1
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
userId | `int64` | 
status | `string` | User health status
