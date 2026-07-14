import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAppDispatch, useAppSelector } from '../hooks';
import { loginUser, registerUser, clearError } from '../redux/slices/authSlice';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import { Sparkles, ArrowRight } from 'lucide-react';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

const registerSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  organization_name: z.string().min(2, 'Organization name must be at least 2 characters'),
});

type LoginFormValues = z.infer<typeof loginSchema>;
type RegisterFormValues = z.infer<typeof registerSchema>;

const Login: React.FC = () => {
  const [isRegistering, setIsRegistering] = useState(false);
  const dispatch = useAppDispatch();
  const { loading, error } = useAppSelector((state) => state.auth);

  // Form setups
  const {
    register: registerLogin,
    handleSubmit: handleSubmitLogin,
    formState: { errors: loginErrors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const {
    register: registerSignUp,
    handleSubmit: handleSubmitSignUp,
    formState: { errors: signUpErrors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  const onLoginSubmit = (values: LoginFormValues) => {
    dispatch(loginUser(values));
  };

  const onSignUpSubmit = async (values: RegisterFormValues) => {
    const result = await dispatch(registerUser(values));
    if (registerUser.fulfilled.match(result)) {
      // Auto login on successful register
      dispatch(loginUser({ email: values.email, password: values.password }));
    }
  };

  const toggleMode = () => {
    dispatch(clearError());
    setIsRegistering(!isRegistering);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-brand-50/50 p-4 font-sans">
      <div className="w-full max-w-[440px] bg-white border border-slate-100 rounded-2xl shadow-xl p-8">
        {/* Title */}
        <div className="flex flex-col items-center text-center mb-8">
          <div className="bg-brand-500 text-white p-2.5 rounded-xl shadow-md flex items-center justify-center mb-3">
            <Sparkles size={24} className="fill-white/10" />
          </div>
          <h1 className="text-xl font-bold text-slate-800 tracking-tight">
            {isRegistering ? 'Create your account' : 'Welcome to HireMind AI'}
          </h1>
          <p className="text-[12px] text-slate-400 mt-1 font-medium">
            {isRegistering ? 'Sign up to start automated resume screening' : 'Sign in to access your recruitment workspace'}
          </p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 text-xs px-4 py-3 rounded-lg border border-red-100 mb-5 font-semibold">
            {error}
          </div>
        )}

        {isRegistering ? (
          /* Register Form */
          <form onSubmit={handleSubmitSignUp(onSignUpSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-3.5">
              <Input
                label="First Name"
                placeholder="e.g. John"
                error={signUpErrors.first_name?.message}
                {...registerSignUp('first_name')}
              />
              <Input
                label="Last Name"
                placeholder="e.g. Doe"
                error={signUpErrors.last_name?.message}
                {...registerSignUp('last_name')}
              />
            </div>
            <Input
              label="Organization Name"
              placeholder="e.g. Acme Inc"
              error={signUpErrors.organization_name?.message}
              {...registerSignUp('organization_name')}
            />
            <Input
              label="Email Address"
              placeholder="name@company.com"
              error={signUpErrors.email?.message}
              {...registerSignUp('email')}
            />
            <Input
              label="Password"
              type="password"
              placeholder="At least 6 characters"
              error={signUpErrors.password?.message}
              {...registerSignUp('password')}
            />
            <Button type="submit" variant="primary" className="w-full py-2.5 font-bold" isLoading={loading}>
              Create Account
            </Button>
          </form>
        ) : (
          /* Login Form */
          <form onSubmit={handleSubmitLogin(onLoginSubmit)} className="space-y-4">
            <Input
              label="Email Address"
              placeholder="name@company.com"
              error={loginErrors.email?.message}
              {...registerLogin('email')}
            />
            <Input
              label="Password"
              type="password"
              placeholder="Your password"
              error={loginErrors.password?.message}
              {...registerLogin('password')}
            />
            <Button type="submit" variant="primary" className="w-full py-2.5 font-bold gap-1.5" isLoading={loading}>
              <span>Sign In</span>
              <ArrowRight size={15} />
            </Button>
          </form>
        )}

        {/* Separator / Toggle link */}
        <div className="mt-6 pt-5 border-t border-slate-50 text-center">
          <button onClick={toggleMode} className="text-xs text-brand-600 hover:text-brand-700 font-bold">
            {isRegistering ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
