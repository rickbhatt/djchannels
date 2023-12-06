import { createSlice } from "@reduxjs/toolkit";
import Cookies from "js-cookie";
import { loginAction } from "../actions/authActions";

const initialState = {
  status: Cookies.get("refresh_token") ? "success" : "loading",
  isAuthenticated: Cookies.get("refresh_token") ? true : false,
  refresh_token: Cookies.get("refresh_token")
    ? Cookies.get("refresh_token")
    : null,

  // access pass
  access_token: Cookies.get("access_token")
    ? Cookies.get("access_token")
    : null,

  user: null,

  error: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loginAction.fulfilled, (state, action) => {
        try {
          const { payload } = action;
          state.status = "success";
          state.isAuthenticated = true;
          state.refresh_token = Cookies.get("refresh_token");
          state.access_token = Cookies.get("access_token");
          state.user = payload.user;
          state.error = null;
        } catch (error) {
          console.log(error);
        }
      })
      .addCase(loginAction.rejected, (state, action) => {
        const { payload } = action;
        state.status = "failed";
        state.error = payload.data;
      });
  },
});

export const getUser = (state) => state.auth.user;
export const getAuthStatus = (state) => state.auth.isAuthenticated;

export default authSlice.reducer;
