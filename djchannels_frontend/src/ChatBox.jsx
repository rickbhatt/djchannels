import { useEffect, useState } from "react";
import useWebSocket from "react-use-websocket";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { ToastAction } from "./components/ui/toast";
import { useToast } from "./components/ui/use-toast";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "react-query";
import axiosInstance, { baseWs } from "./axiosInstance";
import Chats from "./components/Chats";

const ChatBox = () => {
  const [clientMessage, setClientMessage] = useState("");
  const [chatMessages, setChatMessages] = useState([]);

  const { toast } = useToast();

  const { groupName } = useParams();

  const navigate = useNavigate();

  if (!groupName || groupName === "unidentified") {
    navigate(`/`);
  }

  const [socketUrl, setSocketUrl] = useState(
    `${baseWs}/chatapp/async/${groupName}/`
  );

  const {
    sendMessage,
    lastMessage,
    readyState,
    sendJsonMessage,
    lastJsonMessage,
  } = useWebSocket(socketUrl, {
    onOpen: (e) => {
      console.log("Connected to django");
      // sendMessage("Connection is successful, ready to recieve payload");
    },
    queryParams: {
      token: "jkdsakljsasaksdjshduhqhjsjdnasndjdnjsdknsd-rick",
    },
    onMessage: (response) => {},
    onClose: (e) => {
      // console.log(e);
    },
    shouldReconnect: (closeEvent) => true,
    onError: (e) => {
      console.log(e);
    },
  });

  const fetchChat = useQuery(
    ["chat/fetchChat", groupName],
    () =>
      axiosInstance.get(
        `http://127.0.0.1:8000/api/chatapp/get-chats/${groupName}/`
      ),
    {
      enabled: true,
      retry: false,
      refetchOnWindowFocus: false,
      onSuccess: (response) => {
        let chatMsgs = response.data.map((msg) => {
          return msg.content;
        });

        setChatMessages(chatMsgs);
      },
      onError: (error) => {
        console.log(error.response);
      },
    }
  );

  const handleSendMessage = (e) => {
    // sendMessage(clientMessage);
    e.preventDefault();
    if (clientMessage !== "") {
      sendJsonMessage({
        message: clientMessage,
      });
      setClientMessage("");
    } else {
      toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "Chatbox cannot be empty",
        action: <ToastAction altText="Try again">Try again</ToastAction>,
      });
    }
  };

  const handleMessageChange = (e) => {
    setClientMessage(e.target.value);
  };

  useEffect(() => {
    if (lastJsonMessage !== null) {
      setChatMessages((prev) => [...prev, lastJsonMessage.message]);
    }
  }, [lastJsonMessage]);

  return (
    <div className="flex flex-col items-center p-8 gap-5 w-3/5 max-h-screen overflow-y-auto">
      <div className="flex">
        <h2 className="font-bold text-xl">Chatting in group: {groupName}</h2>
      </div>
      <div className="flex flex-col gap-3  w-full overflow-y-auto ">
        <Chats chatMessages={chatMessages} />
      </div>
      <form onSubmit={handleSendMessage} className="flex gap-3 w-full">
        <Input
          value={clientMessage}
          onChange={handleMessageChange}
          type="text"
          placeholder="Enter message"
        />
        <Button type="submit">Send Message</Button>
      </form>
    </div>
  );
};

export default ChatBox;
