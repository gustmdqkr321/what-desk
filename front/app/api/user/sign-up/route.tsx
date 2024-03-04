//signforms/src/app/api/user/sign-up/route.tsx

const handleSubmit = async (id: string, password: string, confirmPassword: string, setError: (error: string) => void) => {
  // 비밀번호 확인
  if (password !== confirmPassword) {
    setError('비밀번호가 일치하지 않습니다.');
    return;
  }

  // 회원가입 요청
  try {
    const response = await fetch("http://210.178.142.51:8001/user/sign_up", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id, password }),
    });
    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();

      // 비밀번호 확인
      if (password !== confirmPassword) {
        setError('비밀번호가 일치하지 않습니다.');
        return;
      }

      // 회원가입 요청
      try {
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id, password }),
        });

        if (response.ok) {
          // 회원가입 성공
          console.log('회원가입이 완료되었습니다.');
        } else {
          // 회원가입 실패
          setError('회원가입에 실패했습니다.');
        }
      } catch (error) {
        console.error('회원가입 중 오류 발생:', error);
        setError('회원가입 중 오류가 발생했습니다.');
      }
    };

    if (response.ok) {
      // 회원가입 성공
      console.log('회원가입이 완료되었습니다.');
    } else {
      // 회원가입 실패
      setError('회원가입에 실패했습니다.');
    }
  } catch (error) {
    console.error('회원가입 중 오류 발생:', error);
    setError('회원가입 중 오류가 발생했습니다.');
  }
};

export default handleSubmit;
