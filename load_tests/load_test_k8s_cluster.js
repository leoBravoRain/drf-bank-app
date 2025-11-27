import http from 'k6/http';
import { sleep } from "k6";

export let options = {
    vus: 200,
    duration: "10s"
};

export default function() {
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2NjYzODEzLCJpYXQiOjE3NjQwNzE4MTMsImp0aSI6ImM0M2IwY2UzOTVmNzRhNGFhZWI1NTJhZjU4YzA0NjdiIiwidXNlcl9pZCI6IjEifQ.h2Z6aglPup9U9wW6_zh7VoPAfb7UPxRY7Ja_Bi8WcY4";

  const headers = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };

  // Example GET accounts
  http.get("http://127.0.0.1:51577/api/accounts/", { headers });
    // http.get("https://www.eventi-app.com/")
}
