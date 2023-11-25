"use client"
import { User, axiosInstance, jsonFormat } from '@/utils/DataFetching'
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { AxiosError, AxiosResponse } from 'axios';
import React, { useEffect, useState } from 'react'

export default function Users() {
    const [users,setUsers] = useState<User[] | null>(null);
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
    <div>
        {users && users.map((user)=>(
             <Card sx={{ minWidth: 275 }} key={user._id}>
             <CardContent>
               <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                 username : {user.username}
               </Typography>
               <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                 user full name : {user.full_name}
               </Typography>
               <Typography sx={{ mb: 1.5 }} color="text.secondary">
                 followers : {user.follower_count}
               </Typography>
               <Typography sx={{ mb: 1.5 }} color="text.secondary">
                 posts : {user.media_count}
               </Typography>
             </CardContent>
             <CardActions>
               <Button size="small" href={`/users/${user.username}`}>More Detail</Button>
             </CardActions>
           </Card>
        ))}
    </div>
  )
}
