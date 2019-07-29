import axios from "axios";

const PING_END_POINT = "/ping";

export function testConnection(URL, success, failure) {
  const endPoint = (URL + PING_END_POINT).replace("//ping", "/ping");
  console.log(`Testing to:${endPoint}`);
  axios
    .get(endPoint)
    .then(response => {
      console.log(response);
      if (response.data === "PONG") {
        success();
      } else {
        failure("Invalid Response from Server");
      }
    })
    .catch(error => {
      failure(error.message);
    });
}
