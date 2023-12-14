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

      <div className="flex justify-center items-center h-screen">
        <Outlet />
      </div>
    </>
  );
}

export default App;
