"use client"
import { Post, UserLogin, axiosInstance, jsonFormat } from '@/utils/DataFetching'
import { AxiosError, AxiosResponse } from 'axios';
import React, { useEffect, useState } from 'react'
import { InstagramEmbed } from 'react-social-media-embed';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FavoriteIcon from '@mui/icons-material/Favorite';
import SyncPost from './syncPost';
import AddOldComments from './AddOldComments';
import AnalyzeSentiment from './AnalyzeSentiment';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import VisibilityIcon from '@mui/icons-material/Visibility';
export default function LatestSyncPost() {
    const [post,setPost] = useState<Post | null>(null);
    const [post_pk,set_pk] = useState('')
    const [open, setOpen] = React.useState(false);
    const theme = useTheme();
    const fullScreen = useMediaQuery(theme.breakpoints.down('md'));
  
    const handleClickOpen = () => {
      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };
    useEffect(()=>{
        axiosInstance.get('/get_login_state')
        .then((res:AxiosResponse<jsonFormat<UserLogin>>)=>{
            console.log(JSON.stringify(res.data.data))
            set_pk(res.data.data.latest_sync);
        })
    })
    useEffect(()=>{
        if(post_pk !== ''){
            axiosInstance.get(`/get_post/${post_pk}`)
            .then((res:AxiosResponse<jsonFormat<Post>>)=>{
                setPost(res.data.data);
            })
            .catch((err_res:AxiosError<jsonFormat<Post>>)=>{
                console.log(JSON.stringify(err_res));
            })
        }
    },[post_pk])
  return (
    <div>
        {post && (
            <InstagramEmbed url={`https://www.instagram.com/p/${post.link}/`} width={500} />
        )}
    </div>
  )
}
