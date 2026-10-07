import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAppDispatch, useAppSelector } from '../hooks';
import { loginUser, registerUser, clearError } from '../redux/slices/authSlice';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import { Sparkles, ArrowRight, Lock, UserPlus, AlertCircle } from 'lucide-react';

const loginSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Please enter a valid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

const registerSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Please enter a valid email address'),
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

  React.useEffect(() => {
    dispatch(clearError());
  }, [dispatch]);

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
      dispatch(loginUser({ email: values.email, password: values.password }));
    }
  };

  const handleTabChange = (registering: boolean) => {
    dispatch(clearError());
    setIsRegistering(registering);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-brand-50/40 to-slate-100 p-4 font-sans">
      <div className="w-full max-w-[440px] bg-white border border-slate-100 rounded-3xl shadow-xl p-8 transition-all">
        {/* Brand Logo & Title */}
        <div className="flex flex-col items-center text-center mb-6">
          <div className="bg-brand-600 text-white p-3 rounded-2xl shadow-md flex items-center justify-center mb-3">
            <Sparkles size={24} className="fill-white/10" />
          </div>
          <h1 className="text-xl font-bold text-slate-800 tracking-tight">
            HireMind AI
          </h1>
          <p className="text-xs text-slate-400 mt-1 font-medium">
            AI-Powered Applicant Tracking & Resume Screening System
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="grid grid-cols-2 p-1 bg-slate-100/80 rounded-xl mb-6 text-xs font-bold border border-slate-200/50">
          <button
            type="button"
            onClick={() => handleTabChange(false)}
            className={`py-2 rounded-lg flex items-center justify-center gap-1.5 transition-all ${
              !isRegistering
                ? 'bg-white text-slate-800 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            <Lock size={13} />
            <span>Sign In</span>
          </button>

          <button
            type="button"
            onClick={() => handleTabChange(true)}
            className={`py-2 rounded-lg flex items-center justify-center gap-1.5 transition-all ${
              isRegistering
                ? 'bg-white text-slate-800 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            <UserPlus size={13} />
            <span>Create Account</span>
          </button>
        </div>

        {/* Error Notification Alert */}
        {error && (
          <div className="bg-red-50/90 text-red-600 text-xs px-4 py-3 rounded-xl border border-red-100 mb-5 font-medium flex items-start gap-2 animate-fadeIn">
            <AlertCircle size={16} className="shrink-0 mt-0.5 text-red-500" />
            <span className="flex-1">{error}</span>
          </div>
        )}

        {isRegistering ? (
          /* Register Form */
          <form onSubmit={handleSubmitSignUp(onSignUpSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
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
              placeholder="e.g. Acme Tech"
              error={signUpErrors.organization_name?.message}
              {...registerSignUp('organization_name')}
            />
            <Input
              label="Email Address"
              type="email"
              placeholder="name@company.com"
              error={signUpErrors.email?.message}
              {...registerSignUp('email')}
            />
            <Input
              label="Password"
              type="password"
              placeholder="Minimum 6 characters"
              error={signUpErrors.password?.message}
              {...registerSignUp('password')}
            />
            <Button
              type="submit"
              variant="primary"
              className="w-full py-2.5 font-bold shadow-sm rounded-xl mt-2"
              isLoading={loading}
            >
              Create Account
            </Button>
          </form>
        ) : (
          /* Login Form */
          <form onSubmit={handleSubmitLogin(onLoginSubmit)} className="space-y-4">
            <Input
              label="Email Address"
              type="email"
              placeholder="name@company.com"
              error={loginErrors.email?.message}
              {...registerLogin('email')}
            />
            <Input
              label="Password"
              type="password"
              placeholder="Enter your password"
              error={loginErrors.password?.message}
              {...registerLogin('password')}
            />
            <Button
              type="submit"
              variant="primary"
              className="w-full py-2.5 font-bold gap-1.5 shadow-sm rounded-xl mt-2"
              isLoading={loading}
            >
              <span>Sign In</span>
              <ArrowRight size={15} />
            </Button>
          </form>
        )}

        {/* Footer info */}
        <div className="mt-6 pt-5 border-t border-slate-100 text-center text-slate-400 text-[11px] font-medium">
          Protected by HireMind AI Security & Roles Authentication
        </div>
      </div>
    </div>
  );
};

export default Login;
