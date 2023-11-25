"use client"
import { axiosInstance, jsonFormat } from '@/utils/DataFetching'
import { AxiosResponse } from 'axios'
import Image from 'next/image'
import { ChangeEvent, useEffect, useState } from 'react'
export default function SyncPost() {
    const [data,setData] = useState<jsonFormat|null>(null);
    const [post,setpost] = useState('');
    const setNewpost = (event : ChangeEvent<HTMLInputElement>)=>{
      setpost(event.target.value)
    }
    function sync_user(post : string){
      console.log("do sync")
      axiosInstance.post(`/sync_post/${post}`)
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
        <div>post : {post}</div>
        <input type="text" onChange={setNewpost}/>
        <button className='border' onClick={()=>sync_user(post)}>Sync</button>
        <p>progress</p>
        <div>{data?.progress.percentage}</div>
      </div>
    )
}
