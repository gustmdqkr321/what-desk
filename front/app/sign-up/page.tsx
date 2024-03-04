//signforms/src/app/sign-up/page.tsx


//회원가입 버튼 눌렀을 때 이 페이지로 이동
"use client";
import RegisterForm from './RegisterForm';

const SignUpPage = () => {
  return (
    <div>
      <RegisterForm /> {/* RegisterForm 컴포넌트를 렌더링합니다. */}
    </div>
  );
};

export default SignUpPage;
