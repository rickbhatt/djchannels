import React from "react";

const Chats = ({ chatMessages }) => {
  return (
    <>
      {!!chatMessages?.length &&
        chatMessages.map((msg, index) => (
          <p
            className="text-left bg-stone-100 p-3 rounded-md w-fit"
            key={index}
          >
            {msg}
          </p>
        ))}
    </>
  );
};

export default Chats;
