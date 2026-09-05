import { Mic, Paperclip, Send } from "lucide-react";
import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import sendMessage from "../../features/sendMessage";
import getCurrentUser from "../../features/getCurrentUser";
import { useDispatch } from "react-redux";
import { createConversation } from "../../features/createConversation";
import {
  setSelectedConversation,
  setConvTitle,
  addConversation,
} from "../redux/conversationSlice";
import updateConversation from "../../features/updateConversation";
import {
  Zap,
  MessageSquare,
  Code2,
  FileText,
  Presentation,
  ImageIcon,
  Globe,
  MicOff,
} from "lucide-react";
import {
  setArtifacts,
  setIsLoading,
  setMessages,
  addMessage,
} from "../redux/messageSlice";
import { setUserData } from "../redux/userSlice";
import { useRef } from "react";
import { X } from "lucide-react";


function ChatInput() {
  const [value, setValue] = useState("");
  const [selectedAgent, setSelectedAgent] = useState("Auto");
  const [selectedFile, setSelectedFile] = useState(null);
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);
  const fileRef = useRef(null);
  const { selectedConversation } = useSelector((state) => state.conversation);
  const { isLoading } = useSelector((state) => state.message);
  const sendingRef = useRef(false);
  const [preview, setPreview] = useState(null);
  const baseTextRef = useRef("");
  const dispatch = useDispatch();
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
      let finalTranscript = "";
      let interimTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      // Save confirmed speech so future dictation continues from it
      if (finalTranscript) {
        baseTextRef.current +=
          (baseTextRef.current ? " " : "") + finalTranscript.trim();
      }

      // Show confirmed + current interim speech
      setValue(
        baseTextRef.current +
          (interimTranscript ? " " + interimTranscript.trim() : ""),
      );
    };

    recognition.onend = () => {
      setListening(false);
    };
    recognition.onerror = (event) => {
      console.error(event.error);
      setListening(false);
    };

    recognitionRef.current = recognition;

    return () => {
      recognition.stop();
    };
  }, []);
  const toggleMic = () => {
    if (!recognitionRef.current) {
      alert("Speech Recognition not supported in this browser.");
      return;
    }

    if (listening) {
      recognitionRef.current.stop();
      setListening(false);
    } else {
      // Save whatever is currently in the textarea
      baseTextRef.current = value.trim();

      try {
        recognitionRef.current.start();
        setListening(true);
      } catch (err) {
        console.error(err);
      }
    }
  };
  //const handleSendMessage = async () => { let conversation = selectedConversation; dispatch(setIsLoading(true)); if (!conversation) { dispatch(setMessages([])); const conv = await createConversation(); dispatch(setSelectedConversation(conv)); dispatch(addConversation(conv)); conversation = conv; } if (conversation.title == "New Chat") { await updateConversation({ id: conversation._id, title: value.trim() }); dispatch( setConvTitle({ conversationId: conversation?._id, title: value.slice(0, 40), }), ); } console.log("selectedFile", selectedFile); const formData = new FormData(); formData.append("prompt", value.trim()); formData.append("conversationId", conversation?._id); formData.append("agent", selectedAgent.toLowerCase()); if (selectedFile) { formData.append("file", selectedFile); } dispatch(addMessage({ role: "user", content: value.trim() })); setValue(""); const data = await sendMessage(formData); dispatch(setIsLoading(true)); setSelectedFile(null); dispatch(setArtifacts(data?.artifacts || [])); dispatch( addMessage({ role: "assistant", content: data?.answer, images: data?.images, }), ); console.log("sendMessage data", data); };
  const handleSendMessage = async () => {
    if (listening && recognitionRef.current) {
      recognitionRef.current.stop();
      setListening(false);
    }
    if (!value.trim() && !selectedFile) return;
    let conversation = selectedConversation;
    if (sendingRef.current) return;

    sendingRef.current = true;
    try {
      dispatch(setIsLoading(true));

      if (!conversation) {
        dispatch(setMessages([]));
        const conv = await createConversation();
        dispatch(setSelectedConversation(conv));
        dispatch(addConversation(conv));
        conversation = conv;
      }

      if (conversation.title === "New Chat") {
        await updateConversation({
          id: conversation._id,
          title: value.trim(),
        });

        dispatch(
          setConvTitle({
            conversationId: conversation._id,
            title: value.slice(0, 40),
          }),
        );
      }

      const formData = new FormData();
      formData.append("prompt", value.trim());
      formData.append("conversationId", conversation._id);
      formData.append("agent", selectedAgent.toLowerCase());

      if (selectedFile) {
        formData.append("file", selectedFile);
      }

      const fileData = selectedFile
        ? {
            name: selectedFile.name,
            type: selectedFile.type,
            size: selectedFile.size,
            preview: preview,
          }
        : null;

      dispatch(
        addMessage({
          role: "user",
          content: value.trim(),
          file: fileData,
        }),
      );

      // Clear the input immediately
      setValue("");
      baseTextRef.current = "";
      setSelectedFile(null);
      if (fileRef.current) {
        fileRef.current.value = null;
      }

      // Then send the request
      const data = await sendMessage(formData);

      dispatch(setArtifacts(data?.artifacts || []));

      dispatch(
        addMessage({
          role: "assistant",
          content: data?.answer,
          images: data?.images,
        }),
      );

      // Credit deductions update the server-side session. Refresh the user in
      // Redux so every balance display receives the authoritative new value.
      const currentUser = await getCurrentUser();
      if (currentUser) {
        dispatch(setUserData(currentUser));
      }

      console.log("sendMessage data", data);
    } catch (err) {
      console.error(err);
    } finally {
      sendingRef.current = false;
      dispatch(setIsLoading(false));
    }
  };

  useEffect(() => {
    if (!selectedFile) {
      setPreview(null);
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);

    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [selectedFile]);

  const agents = [
    {
      id: "auto",
      icon: Zap,
      label: "Auto",
    },
    {
      id: "chat",
      icon: MessageSquare,
      label: "Chat",
    },

    {
      id: "coding",
      icon: Code2,
      label: "Coding",
    },
    {
      id: "pdf",
      icon: FileText,
      label: "PDF",
    },

    {
      id: "ppt",
      icon: Presentation,
      label: "PPT",
    },

    {
      id: "image",
      icon: ImageIcon,
      label: "Image",
    },

    {
      id: "search",
      icon: Globe,
      label: "Search",
    },
  ];

  return (
    <div className="w-full overflow-hidden px-3 md:px-5 py-4 border-t border-white/[0.06] bg-[#0d0f14]">
      <div className="flex flex-col gap-2 bg-white/[0.03] border border-white/[0.07] rounded-2xl px-4 pt-3.5 pb-3">
        <div className="flex w-[80%] gap-2 pr-2 flex-wrap">
          {agents.map((agent) => {
            const isActive = selectedAgent == agent.label;
            const Icon = agent.icon;
            return (
              <div
                key={agent.id}
                className={`flex-shrink-0 inline-flex items-center gap-1.5 px-3 py-2 rounded-full text-xs font-medium transition-all border cursor-pointer
                     ${isActive ? "bg-gradient-to-r from-indigo-500 to-violet-600 text-white border-transparent shadow-[0_1px_8px_rgba(99,102,241,0.35)]" : "bg-white/[0.03] text-slate-400 border-white/[0.06] hover:bg-white/[0.07]"}`}
                onClick={() => setSelectedAgent(agent.label)}
              >
                <Icon
                  size={14}
                  className={isActive ? "text-white" : "text-slate-500"}
                />
                <span className="text-[12px]">{agent.label}</span>
              </div>
            );
          })}
        </div>

        {selectedFile && (
          <div className="my-3">
            <div className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.04] px-3 py-2">
              {selectedFile.type === "application/pdf" ? (
                <FileText size={16} className="text-red-400" />
              ) : (
                selectedFile.type.startsWith("image/") && (
                  <img
                    src={preview}
                    alt="Preview"
                    className="h-10 w-10 rounded-xl object-cover mt-3"
                  />
                )
              )}
              <div>
                <p className="text-xs text-white">{selectedFile?.name}</p>
                <p className="text-[10px] text-slate-500">
                  {Math.ceil(selectedFile.size / 1024)}KB
                </p>
              </div>
              <button
                className="ml-2"
                onClick={() => {
                  setSelectedFile(null);
                  fileRef.current.value = null;
                }}
              >
                <X size={14} className="text-slate-500 hover:text-white" />
              </button>
            </div>
          </div>
        )}
        <textarea
          placeholder="Ask Anything..."
          onChange={(e) => setValue(e.target.value)}
          value={value}
          className="w-full bg-transparent outline-none resize-none text-[14px] text-slate-200 placeholder:text-slate-600 leading-relaxed [scrollbar-width:none] [&::-webkit-scrollbar]:hidden disabled:opacity-50"
          rows={3}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              if (value.trim() || selectedFile) {
                handleSendMessage();
              }
            }
          }}
        />

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1">
            <input
              type="file"
              accept=".pdf,image/*"
              hidden
              ref={fileRef}
              onChange={(e) => {
                const file = e.target.files[0];
                if (file) {
                  setSelectedFile(file);
                }
              }}
            />
            <button
              className="flex items-center justify-center w-8 h-8 rounded-lg text-slate-600 hover:text-slate-400 hover:bg-white/[0.05] border border-transparent hover:border-white/[0.06] transition-all duration-150 bg-transparent cursor-pointer"
              onClick={() => fileRef.current.click()}
              disabled={isLoading}
            >
              <Paperclip size={16} />
            </button>
            <button
              onClick={toggleMic}
              disabled={isLoading}
              className={`flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-150 cursor-pointer
            ${listening ? "bg-red-500 text-white hover:bg-red-700" : "text-slate-600 hover:bg-white/[0.05]"}
            `}
            >
              {listening ? <MicOff size={16} /> : <Mic size={16} />}
            </button>
          </div>

          <button
            disabled={(!value.trim() && !selectedFile) || isLoading}
            onClick={handleSendMessage}
            className={`flex items-center justify-center w-8 h-8 rounded-lg border-none cursor-pointer transition-all duration-150 ${
              (value.trim() || selectedFile) && !isLoading
                ? "bg-linear-to-br from-indigo-500 to-violet-700 hover:opacity-90 text-white"
                : "bg-white/[0.05] text-slate-600 cursor-not-allowed"
            }`}
          >
            <Send size={15} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInput;
