import { React, useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  PanelLeftIcon,
  PanelRight,
  PenSquare,
  Plus,
  MessageSquare,
  User,
  Coins,
  LogOut,
  Menu,
  X,
} from "lucide-react";
import { createConversation } from "../../features/createConversation";
import { getConversations } from "../../features/getConversations";
import {
  addConversation,
  setSelectedConversation,
  setConversations,
} from "../redux/conversationSlice";
import { setUserData } from "../redux/userSlice";
import { logOut } from "../../features/logOut";
import BillingDrawer from "./BillingDrawer";

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const { conversations, selectedConversation } = useSelector(
    (state) => state.conversation,
  );
  const { userData } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const [showBilling, setShowBilling] = useState(false);
  useEffect(() => {
    const getConv = async () => {
      const data = await getConversations();
      dispatch(setConversations(data));
    };
    getConv();
  }, [userData?._id]);
  // const handleCreateConversation = async () => {
  //   const data = await createConversation();
  //   if (data) {
  //     dispatch(addConversation(data));
  //     dispatch(setSelectedConversation(data));
  //   }
  // };

  if (collapsed) {
    return (
      <div className="hidden lg:flex flex-col items-center w-[56px] h-screen bg-[#0d0f14] border-r border-white/10 py-4 gap-1 shrink-0">
        <button
          className="flex items-center justify-center w-9 h-9 rounded-xl text-slate-500 hover:text-slate-200 hover:bg-white/5 transition-colors duration-150 bg-transparent border-none cursor-pointer mb-1"
          onClick={() => setCollapsed(false)}
        >
          <PanelRight />
        </button>

        <button
          className="flex items-center justify-center w-9 h-9 rounded-xl text-slate-500 hover:text-slate-200 hover:bg-white/5 transition-colors duration-150 bg-transparent border-none cursor-pointer"
          onClick={() => dispatch(setSelectedConversation(null))}
        >
          <Plus size={17} />
        </button>
        <div className="flex-1 overflow-y-auto px-2.5 pb-2 scrollbar-width-none [&::-webkit-scrollbar]:hidden pt-5">
          {conversations.map((conv, i) => {
            const isActive = selectedConversation?._id === conv?._id;

            return (
              <div
                key={conv._id || i}
                onClick={() => dispatch(setSelectedConversation(conv))}
                className={`flex items-center gap-2.5 cursor-pointer mb-0.5 px-3 py-2.5 rounded-[10px] border transition-colors duration-150 
                ${
                  isActive
                    ? "bg-indigo-500/10 border-indigo-500/20"
                    : "bg-transparent border-transparent"
                }`}
              >
                <div
                  className={`flex items-center justify-center shrink-0 w-[20px] h-[20px] rounded-lg transition-colors duration-150 ${
                    isActive
                      ? "bg-indigo-500/15 text-indigo-400"
                      : "bg-white/[0.05] text-slate-500"
                  }`}
                >
                  <MessageSquare size={13} />
                </div>
              </div>
            );
          })}
        </div>
        <div className="relative shrink-0">
          {userData?.avatar && !imageError ? (
            <img
              src={userData.avatar}
              alt="User"
              onError={() => setImageError(true)}
              className="w-9 h-9 rounded-[10px] object-cover border-2 border-indigo-500/20"
            />
          ) : (
            <div className="w-9 h-9 rounded-[10px] bg-white/[0.06] flex items-center justify-center">
              <User size={18} className="text-slate-400" />
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <>
      <button
        className="lg:hidden fixed top-3.5 left-4 z-50 flex items-center justify-center w-8 h-8 rounded-lg bg-[#0d0f14] border border-white/[0.06] text-slate-400 hover:text-slate-200 transition-colors duration-150 cursor-pointer"
        onClick={() => setMobileOpen(true)}
      >
        <Menu size={14} />
      </button>
      {mobileOpen && (
        <div
          onClick={() => setMobileOpen(false)}
          className="lg:hidden fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
        />
      )}
      <div
        className={`fixed lg:static inset-y-0 left-0 z-50
    w-[270px] h-screen shrink-0
    bg-[#0d0f14] border-r border-white/[0.06]
    transition-transform duration-250
    ${mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center gap-2.5 px-4 py-4 border-b border-white/[0.06]">
            <div
              className="hidden lg:flex items-center justify-center w-7 h-7 rounded-lg text-slate-500 hover:text-slate-200 hover:bg-white/[0.05] transition-colors duration-150 bg-transparent border-none cursor-pointer"
              onClick={() => setCollapsed(!collapsed)}
            >
              <PanelLeftIcon />
            </div>
            <button
              onClick={() => setMobileOpen(false)}
              className="lg:hidden flex items-center justify-center w-7 h-7 rounded-lg text-slate-500 hover:text-slate-200 hover:bg-white/[0.05] transition-colors duration-150 bg-transparent border-none cursor-pointer"
            >
              <X size={18} />
            </button>

            <span className="text-[16px] font-semibold text-slate-100 tracking-tight flex-1">
              GarvisAI
            </span>
            <span className="text-[10px] font-medium text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded-full tracking-wide">
              {userData?.plan || "free"}
            </span>

            <button
              className="flex items-center justify-center w-7 h-7 rounded-lg text-slate-500 hover:text-slate-200 hover:bg-white/[0.05] transition-colors duration-150 bg-transparent border-none cursor-pointer"
              onClick={() => dispatch(setSelectedConversation(null))}
            >
              <PenSquare size={14} />
            </button>
          </div>
          <div className="px-4 pt-4 pb-1">
            <button
              className="w-full flex items-center justify-center gap-2 text-sm font-medium text-white bg-gradient-to-br from-indigo-500 to-violet-700 rounded-xl py-[10px] border-none cursor-pointer hover:opacity-90 transition-opacity duration-150"
              onClick={() => dispatch(setSelectedConversation(null))}
            >
              <Plus size={15} />
              New Chat
            </button>
          </div>
          {conversations?.length == 0 ? (
            <div className="px-5 pt-4 pb-1.5 text-[10.5px] font-semibold uppercase tracking-widest text-slate-600">
              No Recent Conversations
            </div>
          ) : (
            <div className="px-5 pt-4 pb-1.5 text-[10.5px] font-semibold uppercase tracking-widest text-slate-600">
              Recents
            </div>
          )}
          <div className="flex-1 overflow-y-auto px-2.5 pb-2 scrollbar-width-none [&::-webkit-scrollbar]:hidden">
            {conversations?.map((conv, i) => {
              const isActive = selectedConversation?._id === conv?._id;

              return (
                <div
                  key={conv._id || i}
                  onClick={() => dispatch(setSelectedConversation(conv))}
                  className={`flex items-center gap-2.5 cursor-pointer mb-0.5 px-3 py-2.5 rounded-[10px] border transition-colors duration-150 
                ${
                  isActive
                    ? "bg-indigo-500/10 border-indigo-500/20"
                    : "bg-transparent border-transparent"
                }`}
                >
                  <div
                    className={`flex items-center justify-center shrink-0 w-[28px] h-[28px] rounded-lg transition-colors duration-150 ${
                      isActive
                        ? "bg-indigo-500/15 text-indigo-400"
                        : "bg-white/[0.05] text-slate-500"
                    }`}
                  >
                    <MessageSquare size={13} />
                  </div>

                  <span
                    className={`text-[13px] font-medium truncate ${
                      isActive ? "text-slate-100" : "text-slate-300"
                    }`}
                  >
                    {conv?.title || "New Chat"}
                  </span>
                </div>
              );
            })}
          </div>
          <div className="mx-2.5 h-px bg-white/[0.06]" />
          <div className="px-3.5 py-3.5">
            {userData ? (
              <div className="flex items-center gap-2.5 cursor-pointer rounded-xl px-3 py-2.5 hover:bg-white/[0.05] transition-colors duration-150">
                <div className="relative shrink-0">
                  {userData?.avatar && !imageError ? (
                    <img
                      src={userData.avatar}
                      alt="User"
                      onError={() => setImageError(true)}
                      className="w-9 h-9 rounded-[10px] object-cover border-2 border-indigo-500/20"
                    />
                  ) : (
                    <div className="w-9 h-9 rounded-[10px] bg-white/[0.06] flex items-center justify-center">
                      <User size={18} className="text-slate-400" />
                    </div>
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <p className="text-[13.5px] font-semibold text-slate-100 truncate">
                    {userData?.name || "User"}
                  </p>
                  <p className="text-[11px] text-slate-600 mt-px">
                    {`${userData?.plan}` || "free "}
                  </p>
                </div>
                <div className="flex gap-1">
                  <button
                    className="flex items-center justify-center w-7 h-7 rounded-[7px] border-none bg-transparent text-yellow-600 cursor-pointer hover:bg-white/[0.05] hover:text-slate-400 transition-all duration-150"
                    onClick={() => setShowBilling(true)}
                  >
                    <Coins size={16} />
                  </button>

                  <button
                    className="flex items-center justify-center w-7 h-7 rounded-[7px] border-none bg-transparent text-slate-600 cursor-pointer hover:bg-white/[0.05] hover:text-slate-400 transition-all duration-150"
                    onClick={() => {
                      logOut();
                      dispatch(setUserData(null));
                    }}
                  >
                    <LogOut size={16} />
                  </button>
                </div>
              </div>
            ) : (
              <button className="w-full rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white py-2.5 font-medium transition-colors">
                Login
              </button>
            )}
          </div>
        </div>
        
      </div>
      <BillingDrawer
          open={showBilling}
          onClose={() => setShowBilling(false)}
        />
    </>
  );
}

export default Sidebar;
