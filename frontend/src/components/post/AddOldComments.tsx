"use client"
import { Post, axiosInstance, jsonFormat } from '@/utils/DataFetching';
import React from 'react'
import { AxiosResponse } from 'axios'
import { useState } from 'react'
import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';
import AddIcon from '@mui/icons-material/Add';
interface PostSet{
    posts : Post[];
    setPosts : React.Dispatch<React.SetStateAction<Post[] | null>>;
    index : number;
}
export default function AddOldComments({posts,setPosts,index}:PostSet) {
    const [isSync,setSync] = useState(false);
    function sync_post(e : any){
      setSync(true);
      axiosInstance.post(`/get_past_comments/${posts[index].post_pk}`)
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
        {isSync ? (<CircularProgress/>):(<AddIcon/>)}
      </IconButton>
      
    )
}
