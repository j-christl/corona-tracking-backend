# corona-tracking-backend
Backend of the Corona Tracking App, developed in the context of the #WirVsVirus Hackathon by the german government. See https://wirvsvirushackathon.org/

# Dependencies
- Python 3.7
- websockets
- psycopg2-binary

# REST API Documentation
- Content-Type must be application/json
```
GET /test
```
Just for testing
```
POST /register
```
Register user.

```
POST /contacts
```
Upload contacts.

**Request body:**
```
{
  [
    {
        timestamp: 123456
        contactId0: 123456
        contactId1: 123456
    }
    ...
  ]
}
```