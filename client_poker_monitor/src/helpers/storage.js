import AsyncStorage from "@react-native-community/async-storage";

const DEFAULT_URL = "http://poker_app.ddns.net:80/";

export async function getDefaultURL() {
  const value = await AsyncStorage.getItem("@DEFAULT_URL");
  if (value) {
    return value;
  } else {
    await AsyncStorage.setItem("@DEFAULT_URL", DEFAULT_URL);
    const newStoredValue = await AsyncStorage.getItem("@DEFAULT_URL");
    return newStoredValue;
  }
}
