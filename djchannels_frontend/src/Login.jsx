import { Button } from "./components/ui/button";
import { Link, useNavigate } from "react-router-dom";
import { Input } from "./components/ui/input";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { loginAction } from "./redux/actions/authActions";
const Login = () => {
  const initialFormState = {
    email: "",
    password: "",
  };

  const [formData, setFormData] = useState(initialFormState);

  const handleFormChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { email, password } = formData;
    try {
      let response = await dispatch(loginAction({ email, password })).unwrap();
      navigate(`select-group`, { replace: true });
    } catch (error) {}
  };

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
