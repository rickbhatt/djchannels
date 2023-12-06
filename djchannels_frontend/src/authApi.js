import axiosInstance from "./axiosInstance";

export const handleLogin = async (email, password) => {
  try {
    let response = await axiosInstance.post(`/account/login/`, {
      email: email,
      password: password,
    });

    return response;
  } catch (error) {
    console.log(error);
  }
};
