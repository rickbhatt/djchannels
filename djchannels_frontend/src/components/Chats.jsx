import React from "react";

const Chats = ({ chatMessages }) => {
  return (
    <>
      {!!chatMessages?.length &&
        chatMessages.map((msg, index) => (
          <p
            className="flex flex-col text-left bg-stone-100 p-3 rounded-md w-fit"
            key={index}
          >
            <span className="font-bold text-sm">{msg.user}</span>
            {msg.message}
          </p>
        ))}
    </>
  );
};

export default Chats;
