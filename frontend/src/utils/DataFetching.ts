import axios, { AxiosError, AxiosResponse } from 'axios';

export const axiosInstance = axios.create({
    baseURL: `http://127.0.0.1:5000/api`,
    withCredentials: true,
});
export interface User {
    _id: string;
    user_pk: string;
    username: string;
    full_name: string;
    media_count: number;
    follower_count: number;
    pfp_url: string;
    posts: string[];
    end_cursor: null | string; // Assuming it can be null or a string
    last_sync: string;

}
export interface Post {
    _id: string;
    username: string;
    link: string;
    post_pk: string;
    caption: string;
    comment_disabled: boolean;
    comments_total: number;
    likes_total: number;
    media_type: number;
    product_type: string;
    thumbnail_url: string;
    view_count: number;
    video_url: null | string;
    comments: Comment[];
    engagement_rate : [{
        engagement_rate_score : number;
        datetime : Date;
    }]
    end_cursor: null | string;
    last_sync: string;
}
interface Comment {
    comment_pk: string;
    username: string;
    text: string;
    sentiment?:{
        overall : number;
        detail : {
            positive : number;
            neutral : number;
            negative : number;
        }
    }
}
export interface DataProgress{
    _id: string;
    process : string;
    progress : number;
    is_done : boolean;
}
export interface jsonFormat<T>{
        status: {
            code: string,
            message:string
        },
        progress: {
            percentage: number,
            is_done: boolean
        },
        data: T
}
export interface UserLogin {
    _id: {
      $oid: string;
    };
    username: string;
    password: string;
    is_logged: boolean;
  }