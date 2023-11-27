"use client"
import { Post, axiosInstance, jsonFormat } from '@/utils/DataFetching'
import { AxiosResponse } from 'axios'
import Image from 'next/image'
import { ChangeEvent, useEffect, useState } from 'react'
import SyncIcon from '@mui/icons-material/Sync';
import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';
interface setPost {
  posts : Post[];
  setPosts : React.Dispatch<React.SetStateAction<Post[] | null>>;
  index : number;
}
export default function SyncPost({posts,setPosts, index} : setPost) {
  const [isSync,setSync] = useState(false);
    function sync_post(e : any){
      setSync(true);
      axiosInstance.post(`/sync_post/${posts[index].post_pk}`)
        .then((response : AxiosResponse<jsonFormat<Post>>)=>{
          const newPost = response.data.data;
          const newPosts = [...posts]
          newPosts[index] = newPost;
          setPosts(newPosts)
          setSync(false);
        })
        .catch((err_response)=>{
          console.log(err_response)
        })
    }
    return (
      <IconButton color="primary" aria-label="sync" className={`p-0 rounded-full hover:bg-sky-300`} onClick={sync_post}>
        {isSync ? (<CircularProgress/>):(<SyncIcon/>)}
      </IconButton>
      
    )
}
