# songstorm-server

## API DOCS

These are the API endpoints available to the client iOS and Android Apps

### /api/link

**Method**: `GET`

**Params**:
- title : `string`

**Response**: `JSON`
```
{
  link: string
}
```

### /api/send

**Method**: `POST`

**Params**:
- link : `string`
- uid : `int`

**Response**: `200`

### /api/listening

**Method**: `POST`

**Params**:
- songid : `string`
- uid : `int`
- location : `JSON{lat: float, loc: float}`

**Response**: `200`

### /api/near

**Method**: `GET`

**Params**:
- lat : `float`
- lon : `float`
- radius : `float`

**Response**: `array of JSON`

```
[
  {
    uid: int,
    song: string
    songid: string
  }
]
```

### /song

**Method**: `GET`

**Params**:
- songid: `string`

**Response**: `text/html`
