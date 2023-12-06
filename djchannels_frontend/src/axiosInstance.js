import axios from "axios";
import { jwtDecode } from "jwt-decode";
import dayjs from "dayjs";
import Cookies from "js-cookie";
import store from "./redux/store/store";
import { updateAuthState } from "./redux/slices/authSlice";

export const baseURL = "http://127.0.0.1:8000/api";

export const baseWs = "ws://127.0.0.1:8000/ws";

const axiosInstance = axios.create({
  baseURL: baseURL,
  timeout: 60 * 10000,
  withCredentials: true,
  headers: {
    Authorization: Cookies.get("access_token")
      ? `Bearer ${Cookies.get("access_token")}`
      : null,

    "Content-Type": "application/json",
    accept: "application/json",
  },
});

axiosInstance.interceptors.request.use(async (req) => {
  const refreshToken = Cookies.get("refresh_token");

  /*
    CHECKING IF REFRESH TOKEN IS PRESENT
    IF NOT THAT MEANS THE USER IS NOT LOGGED
    IN AND REQUIRES NO AUTHORIZATION HEADER
  */
  if (!refreshToken) {
    req.headers.Authorization = "";
    return req;
  }

  /*
    CHECK WHETHER ACCESS TOKEN EXISTS AND 
    IF IT HAS EXPIRED
  */

  const accessToken = Cookies.get("access_token");

  if (accessToken) {
    const decodedToken = jwtDecode(accessToken);
    const isExpired = dayjs.unix(decodedToken.exp).diff(dayjs()) < 1;

    if (!isExpired) {
      req.headers.Authorization = `Bearer ${accessToken}`;
      return req;
    }
  }

  /*
    REQUESTING FOR A NEW ACCESS TOKEN
  */

  try {
    const response = await axios.post(
      `${baseURL}/account/token/refresh/`,
      {
        refresh: refreshToken,
      },
      { withCredentials: true }
    );

    store.dispatch(updateAuthState());
    req.headers.Authorization = `Bearer ${Cookies.get("access_token")}`;
    return req;
  } catch (error) {
    console.log(error);
  }
});

export default axiosInstance;
