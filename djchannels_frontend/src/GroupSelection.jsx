import { Button } from "./components/ui/button";
import { Link } from "react-router-dom";
import { Input } from "./components/ui/input";
import { useState } from "react";

const GroupSelection = () => {
  const [groupName, setGroupName] = useState("");

  const handleGroupName = (e) => {
    setGroupName(e.target.value);
  };

  return (
    <div className="flex flex-col gap-5 w-96">
      <Input
        value={groupName}
        onChange={handleGroupName}
        type="text"
        placeholder="Enter group name to join"
      />
      <Button asChild>
        <Link to={`chat/${groupName}`}>Join Group</Link>
      </Button>
    </div>
  );
};

export default GroupSelection;
