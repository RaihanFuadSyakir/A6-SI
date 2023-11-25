"use client"
import BreadCrumbs from '@/components/etc/BreadCrumbs';
import UserProfile from '@/components/user/UserProfile'
import { usePathname } from 'next/navigation'
import React from 'react'

export default function User({ params }: { params: { slug: string }}) {
    const pathname = usePathname();
  return (
    <div>
        <BreadCrumbs path={pathname}/>
        <UserProfile username={params.slug}/>
    </div>
  )
}
