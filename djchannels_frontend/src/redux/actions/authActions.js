import axiosInstance from "@/axiosInstance";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const loginAction = createAsyncThunk(
  "auth/login",
  async ({ email, password }, { rejectWithValue }) => {
    try {
      let response = await axiosInstance.post(`/account/login/`, {
        email: email,
        password: password,
      });
      return response.data;
    } catch (error) {
      if (error.response) {
        return rejectWithValue(error.response);
      }

      rejectWithValue("Some problem with request");
    }
  }
);
