//signforms/src/app/pages/login.tsx

"use client";


import React, { useState } from 'react';
import { signIn, signOut, useSession } from 'next-auth/react';

const Avatar = ({ children }) => <div>{children}</div>; // Placeholder for Avatar component
const AvatarImage = ({ src, alt }) => <img src={src} alt={alt} />; // Placeholder for AvatarImage component
const AvatarFallback = ({ children }) => <div>{children}</div>; // Placeholder for AvatarFallback component

const LoginButton = () => {
  const { data } = useSession();

  const onClick = async (e: React.MouseEvent) => {
    e.preventDefault();

    if (data) {
      await signOut();
    } else {
      try {
        await signIn();
      } catch (error) {
        alert(error.message);
      }
    }
  }

  return (
    <div className="flex items-center gap-3">
      {data?.user && (
        <Avatar>
          <AvatarImage src={data.user.image ?? ""} alt="user image" />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
      )}
      <a href="#" onClick={onClick} className="text-sm text-white">{data ? "로그아웃" : "로그인하기"}</a>
      <a href="/sign-up" className="text-sm text-white">회원가입</a>
    </div>
  );
};

export default LoginButton;
