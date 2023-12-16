import { Button } from "./components/ui/button";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { Input } from "./components/ui/input";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { loginAction } from "./redux/actions/authActions";
import { getAuthStatus } from "./redux/slices/authSlice";
const Login = () => {
  const initialFormState = {
    email: "",
    password: "",
  };

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const authStatus = useSelector(getAuthStatus);

  const [formData, setFormData] = useState(initialFormState);

  const handleFormChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { email, password } = formData;
    try {
      let response = await dispatch(loginAction({ email, password })).unwrap();
      navigate(`/select-group`);
    } catch (error) {}
  };

  if (authStatus) {
    return <Navigate to="/select-group" replace />;
  }

  return (
    <div className="flex flex-col justify-center items-center h-screen gap-5 w-96">
      <form onSubmit={handleSubmit} className="flex flex-col gap-5 w-96">
        <Input
          value={formData.email}
          onChange={handleFormChange}
          type="email"
          name="email"
          placeholder="Enter email"
        />
        <Input
          value={formData.password}
          onChange={handleFormChange}
          type="password"
          name="password"
          placeholder="Enter password"
        />
        <Button type="submit">Login</Button>
      </form>
    </div>
  );
};

export default Login;
