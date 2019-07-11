import axios from "axios";

const pingEndPoint = "/ping";

export function testConnection(URL, success, failure) {
  axios
    .get(URL + pingEndPoint)
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
