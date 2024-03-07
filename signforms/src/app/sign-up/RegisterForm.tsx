// RegisterForm.tsx
import { useState } from 'react';
import handleSubmit from '../api/user/sign-up/route'; // handleSubmit.ts 파일을 가져옴

const RegisterForm = () => {
  const [user_id, setUserid] = useState<string>('');
  const [name, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [image, setImage] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // handleSubmit 함수 호출
    await handleSubmit(user_id, name, email, image, password, confirmPassword, setError);
  };

  return (
    <form onSubmit={onSubmit}>
      <div>
        <label>username:</label>
        <input type="text" value={user_id} onChange={(e) => setUserid(e.target.value)} />
      </div>
      <div>
        <label>비밀번호:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div>
        <label>비밀번호 확인:</label>
        <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
      </div>
      <div>
        <label>닉네임:</label>
        <input type="string" value={name} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>이메일:</label>
        <input type="string" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      {error && <div>{error}</div>}
      <button type="submit">회원가입하기</button>
    </form>
  );
};


export default RegisterForm;
