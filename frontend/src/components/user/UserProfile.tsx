"use client"
import { Post, User, axiosInstance, jsonFormat } from '@/utils/DataFetching'
import { AxiosError, AxiosResponse } from 'axios';
import React, { useEffect, useState } from 'react'
import { InstagramEmbed } from 'react-social-media-embed';
import DialogPost from '../post/DialogPost';
import Button from '@mui/material/Button';
export default function UserProfile({username}:{username : string}) {
  const [user, setUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<Post[] | null>(null);
  const [visiblePosts, setVisiblePosts] = useState<number>(5);

  useEffect(() => {
    axiosInstance
      .get(`/get_userinfo/${username}`)
      .then((response) => {
        setUser(response.data.data);
      })
      .catch((err_response) => {
        console.log(JSON.stringify(err_response.response?.data));
      });
  }, []);

  useEffect(() => {
    axiosInstance
      .get(`/get_user_posts/${username}`)
      .then((response) => {
        setPosts(response.data.data);
      })
      .catch((err_response) => {
        console.log(JSON.stringify(err_response.response?.data));
      });
  }, []);

  const loadMorePosts = () => {
    setVisiblePosts((prevVisiblePosts) => prevVisiblePosts + 5);
  };

  return (
    <div className='m-4'>
      <p>UserProfile</p>
      <p>{user?.username}</p>
      <div className='relative flex flex-wrap'>
        {posts &&
          posts.slice(0, visiblePosts).map((post,index) => (
            <div className='flex flex-col w-[328px] justify-between' key={post.post_pk}>
              <InstagramEmbed url={`https://www.instagram.com/p/${post.link}/`} width={328}/>
              <DialogPost posts={posts} setPosts={setPosts} index={index}/>
            </div>
          ))}
      </div>
      {posts && visiblePosts < posts?.length && (
        <Button 
          variant="contained" 
          className='flex flex-col mt-4 mx-auto justify-center bg-blue-400' 
          onClick={loadMorePosts}>Load More</Button>
      )}
    </div>
  );
}
