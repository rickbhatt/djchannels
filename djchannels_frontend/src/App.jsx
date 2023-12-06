import "./App.css";
import { Helmet } from "react-helmet";
import { Toaster } from "./components/ui/toaster";

import { Outlet } from "react-router-dom";
function App() {
  return (
    <>
      <Toaster />
      <Helmet>
        <title>Chat App</title>
      </Helmet>

      <Outlet />
    </>
  );
}

export default App;
