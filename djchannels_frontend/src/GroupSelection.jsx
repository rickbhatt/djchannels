import { Button } from "./components/ui/button";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { Input } from "./components/ui/input";
import { useState } from "react";

const GroupSelection = () => {
  const [groupName, setGroupName] = useState("");

  const navigate = useNavigate();

  const handleGroupName = (e) => {
    setGroupName(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("submitting");
    navigate(`/chat/${groupName}`);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col justify-center items-center h-screen gap-5 w-96 "
    >
      <Input
        value={groupName}
        onChange={handleGroupName}
        type="text"
        placeholder="Enter group name to join"
      />
      <Button type="submit">Join Group</Button>
    </form>
  );
};

export default GroupSelection;
