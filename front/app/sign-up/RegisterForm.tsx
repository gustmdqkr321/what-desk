//signforms/src/app/sign-up/RegisterForm.tsx

// RegisterForm.tsx
import { useState } from 'react';
import handleSubmit from '../api/user/sign-up/route'; // handleSubmit.ts 파일을 가져옴

const RegisterForm = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // handleSubmit 함수 호출
    await handleSubmit(username, password, confirmPassword, setError);
  };

  return (
    <form onSubmit={onSubmit}>
      <div>
        <label>username:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>비밀번호:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div>
        <label>비밀번호 확인:</label>
        <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
      </div>
      {error && <div>{error}</div>}
      <button type="submit">회원가입</button>
    </form>
  );
};


export default RegisterForm;
