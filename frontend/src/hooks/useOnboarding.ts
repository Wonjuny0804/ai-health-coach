import { useEffect, useState } from "react";

interface OnboardingData {
    sessionId: string;
    status: string;
    currentStepId: string;
    steps: {
        id: string;
        title: string;
        answer: string | null;
        status: string;
        question: string;
    }[];
    payload: {
        kind: string;
        id: string;
        prompt: string;
        placeholder: string;
        required: boolean;
        minLen: number;
        maxLen: number;
    },
    paraphrasedAnswers: unknown // TODO: fix type
}



const useOnboarding = () => {
    const [data, setData] = useState<OnboardingData>();

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch("http://localhost:8000/api/onboarding/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: "Hello",
                }),
            });
            const { data } = await response.json();
            setData(JSON.parse(data));
        }
        fetchData();
    }, []);

    return data;
}

export default useOnboarding;