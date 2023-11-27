"use client"
import { User, axiosInstance, jsonFormat } from '@/utils/DataFetching'
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { AxiosError, AxiosResponse } from 'axios';
import React, { useEffect, useState } from 'react'
import SyncIcon from '@mui/icons-material/Sync';
import SyncUser from '@/components/user/SyncUser';
import AddPastPosts from '@/components/user/AddPastPosts';
import SearchUser from '@/components/user/SearchUser';
export default function Users() {
    const [users,setUsers] = useState<User[]>([]);
    useEffect(()=>{
        axiosInstance.get('/get_users/')
            .then((res : AxiosResponse<jsonFormat<User[]>>)=>{
                setUsers(res.data.data);
            })
            .catch((err_res : AxiosError<jsonFormat<User[]>>)=>{
                console.log(JSON.stringify(err_res.response?.data))
            })
    },[])
  return (
    <div className='m-4'>
      <SearchUser users={users} setUsers={setUsers}/>
      <div className='flex flex-wrap'>
        {users && users.map((user,index)=>(
             <Card sx={{ minWidth: 275 }} key={user._id} className='rounded m-2'>
             <CardContent>
             <Typography variant="h5" component="div">
                 {user.username}
               </Typography>
               <Typography sx={{ mb: 1.5 }} color="text.secondary">
                 {user.full_name}
               </Typography>
               <Typography sx={{ mb: 1.5 }} color="text.secondary">
                 followers : {user.follower_count}
               </Typography>
               <Typography sx={{ mb: 1.5 }} color="text.secondary">
                 posts : {user.media_count}
               </Typography>
               <Typography sx={{ mb: 1.5 }} color="text.secondary">
                 posts stored : {user.posts.length}
               </Typography>
               <Typography variant="body2">Add past posts<AddPastPosts users={users} setUsers={setUsers} index={index}/></Typography>
               <Typography variant="body2">{user.last_sync}<SyncUser users={users} setUsers={setUsers} index={index}/></Typography>
             </CardContent>
             <CardActions>
               <Button size="small" href={`/users/${user.username}`}>More Detail</Button>
             </CardActions>
           </Card>
        ))}
    </div>
    </div>
  )
}
