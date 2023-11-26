"use client"
import React from 'react'
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Post } from '@/utils/DataFetching';
import FavoriteIcon from '@mui/icons-material/Favorite';
import SyncPost from './syncPost';
import AddOldComments from './AddOldComments';
import AnalyzeSentiment from './AnalyzeSentiment';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import VisibilityIcon from '@mui/icons-material/Visibility';
interface showPost{
    posts : Post[];
    setPosts : React.Dispatch<React.SetStateAction<Post[] | null>>;
    index : number;
}
export default function DialogPost({posts,setPosts,index}:showPost) {
    const [open, setOpen] = React.useState(false);
    const theme = useTheme();
    const fullScreen = useMediaQuery(theme.breakpoints.down('md'));
  
    const handleClickOpen = () => {
      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };
  
    return (
      <React.Fragment>
        <Button variant="outlined" onClick={handleClickOpen}>
          Stored Post Data
        </Button>
        <Dialog
          fullScreen={fullScreen}
          open={open}
          onClose={handleClose}
          aria-labelledby="show-post-detail"
        >
          <DialogTitle id="show-post-detail">
            {"Post Detail"}
          </DialogTitle>
          <DialogContent>
          <Typography variant='body1'>{posts[index].caption}</Typography>
            <div className='flex flex-row justify-between'>
                <div className='flex flex-col'>
                    <Typography><VisibilityIcon/>{posts[index].view_count}</Typography>
                    <Typography><FavoriteIcon className='text-red-600'/>{posts[index].likes_total}</Typography>
                    <Typography><ChatBubbleOutlineIcon/> {posts[index].comments_total}</Typography>
                    <Typography>old comments <AddOldComments setPosts={setPosts} posts={posts} index={index}/></Typography>
                    <Typography>Analyze Sentiment <AnalyzeSentiment setPosts={setPosts} posts={posts} index={index}/></Typography>
                    
                </div>
                <Typography className='flex items-end'>
                  <div>
                  <SyncPost posts={posts} setPosts={setPosts} index={index}/>
                  {posts[index].last_sync}
                  </div>
                </Typography>
            </div>
          <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="comments-detail"
          id="comments-header"
        >
          <Typography>Comments : {posts[index].comments.length}</Typography>
        </AccordionSummary>
        <AccordionDetails>
        {posts[index].comments.map((comment,index_c)=>(
            <div className='flex flex-row' key={`${posts[index].post_pk}${index_c}`}>
                <div className='w-1/3 font-bold'>{comment.username}</div>
                <div className='w-2/3 flex flex-col'>
                    <div>{comment.text}</div>
                    <div>{comment.sentiment && (
                        comment.sentiment?.overall === 1 ? 
                        (<div className='text-blue-600'>Posititive</div>) 
                        :
                        (<div className='text-red-600'>Negative</div>)
                    )}
                    </div>
                    {comment.sentiment && comment.sentiment?.detail && (
                        <Accordion className='w-2/3'>
                            <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="sentiment-detail"
                            id="sentiment-header"
                            >
                            <Typography>Detail</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                            <div className='flex flex-col'>
                                    <div className='text-blue-600'>positive : {comment.sentiment?.detail.positive}</div>
                                    <div className='text-red-600'>negative : {comment.sentiment?.detail.negative}</div>
                                    <div className='text-gray-600'>neutral : {comment.sentiment?.detail.neutral}</div>
                            </div>
                            </AccordionDetails>
                        </Accordion>
                    )}
                    
                </div>
            </div>
          ))}
        </AccordionDetails>
      </Accordion>
          
          </DialogContent>
          <DialogActions>
            <Button autoFocus onClick={handleClose}>
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </React.Fragment>
    );
}
