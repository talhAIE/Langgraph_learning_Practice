# Langgraph Execution Model
how langgraph execute workflow

1. Graph Definition

You define:
- The state schema
- Nodes (functions that perform tasks)
- Edges (which node connects to which)

2. Compilation

You call .compile() on the StateGraph. This checks the graph structure and prepares it for execution.

3. Invocation

You run the graph with invoke(initial_state). LangGraph sends the initial state as a message to the entry node(s).

4. Super-Steps Begin

Execution proceeds in rounds.
In each round (super-step):
- All active nodes (those that received messages) run in parallel
- Each returns an update (message) to the state

5. Message Passing & Node Activation

The messages are passed to downstream nodes via edges. Nodes that receive messages become active for the next round.

6. Halting Condition
Execution stops when:
- No nodes are active, and
- No messages are in transit

### Message Parsing
- sending state to next nodes through edges

### super step
 - round by round work

