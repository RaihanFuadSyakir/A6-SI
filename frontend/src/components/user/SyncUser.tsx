"use client"
import { axiosInstance, jsonFormat } from '@/utils/DataFetching'
import { AxiosResponse } from 'axios'
import Image from 'next/image'
import { ChangeEvent, useEffect, useState } from 'react'
export default function SyncUser() {
    const [data,setData] = useState<jsonFormat|null>(null);
    const [username,setUsername] = useState('');
    const setNewUsername = (event : ChangeEvent<HTMLInputElement>)=>{
      setUsername(event.target.value)
    }
    function sync_user(username : string){
      console.log("do sync")
      axiosInstance.post(`/sync_user/${username}`)
        .then((response : AxiosResponse<jsonFormat>)=>{
          console.log("aaa")
          console.log(response)
          setData(response.data)
        })
        .catch((err_response)=>{
          console.log(err_response)
        })
    }
    useEffect(()=>{
  
    },[data])
    return (
      <div className='text-black'>
        <div>username : {username}</div>
        <input type="text" onChange={setNewUsername}/>
        <button className='border' onClick={()=>sync_user(username)}>Sync</button>
        <p>progress</p>
        <div>{data?.progress.percentage}</div>
      </div>
    )
}
