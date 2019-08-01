import axios from "axios";

const PING_END_POINT = "/ping";
const TABLE_END_POINT = "/table";

const axios_instance = axios.create({ timeout: 2000 });

export function testConnection(URL, success, failure) {
  const endPoint = (URL + PING_END_POINT).replace("//ping", "/ping");
  console.log(`Testing to:${endPoint}`);

  axios_instance
    .get(endPoint)
    .then(response => {
      console.log(`Dummy response: ${response.data}`);
    })
    .catch(error => {
      console.log(error.message);
    });

  setTimeout(() => {
    axios_instance
      .get(endPoint)
      .then(response => {
        console.log(`Correct Response:${response.data}`);
        if (response.data === "PONG") {
          success(URL);
        } else {
          failure(URL, "Invalid Response from Server");
        }
      })
      .catch(error => {
        failure(error.message);
      });
  }, 2000);
}

export function getCurrentTable(URL, table_id, success, failure) {
  const endPoint = (URL + TABLE_END_POINT + `/${table_id}`).replace(
    "//table",
    "/table"
  );
  console.log(`Fetching table from :${endPoint}`);
  axios_instance
    .get(endPoint)
    .then(response => {
      success(response.data);
    })
    .catch(error => {
      failure(error.message);
    });
}
