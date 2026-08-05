import React, {useEffect} from 'react'
import ChatInput from './ChatInput'
import MessageList from './MessageList'
import Nav from './Nav'
import { useSelector } from 'react-redux'
import getMessages from '../../features/getMessages'
import { useDispatch } from 'react-redux'
import {setMessages} from '../redux/messageSlice'
import {setArtifacts} from '../redux/messageSlice'



function ChatArea() {
    const {selectedConversation}=useSelector((state)=>state.conversation)
    const dispatch=useDispatch()
    useEffect(() => {
        const getMesg = async () => {
            if(selectedConversation){
                if(selectedConversation.title=="New Chat") return;
                const data=await getMessages(selectedConversation?._id);
                console.log("getMessages data",data)
                dispatch(setMessages(data))
                const latestArtifactMessage=[...data].reverse().find(msg=>msg.artifacts && msg.artifacts.length>0)
                dispatch(setArtifacts(latestArtifactMessage?.artifacts || []))
            }
        }
        getMesg();
    },[selectedConversation?._id])
  return (
    <div className="flex-1 flex flex-col min-w-0">
        <Nav/>
        <MessageList/>
        <ChatInput/>
    </div>
  )
}

export default ChatArea