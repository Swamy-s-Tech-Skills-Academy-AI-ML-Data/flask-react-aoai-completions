import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Chat from '../components/Chat';

// Mock API service
vi.mock('../services/api', () => ({
    fetchAIResponse: async (prompt: string) => ({ response: `Echo: ${prompt}`, usage: { prompt_chars: prompt.length, response_chars: prompt.length + 6 } })
}));

describe('Chat component', () => {
    it('renders initial assistant message', () => {
        render(<Chat />);
        expect(screen.getByText(/Ask me something/i)).toBeInTheDocument();
    });

    it('sends a prompt and displays response', async () => {
        render(<Chat />);
        const textarea = screen.getByPlaceholderText(/Type your question/i);
        fireEvent.change(textarea, { target: { value: 'Hello' } });
        fireEvent.click(screen.getByRole('button', { name: /send/i }));
        await waitFor(() => expect(screen.getByText(/Echo: Hello/)).toBeInTheDocument());
    });
});
