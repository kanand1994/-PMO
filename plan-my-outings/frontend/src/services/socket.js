import io from 'socket.io-client';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5000';

class SocketService {
  constructor() {
    this.socket = null;
  }

  connect() {
    this.socket = io(SOCKET_URL);
    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }

  joinGroup(groupId) {
    if (this.socket) {
      this.socket.emit('join_group', { group_id: groupId });
    }
  }

  leaveGroup(groupId) {
    if (this.socket) {
      this.socket.emit('leave_group', { group_id: groupId });
    }
  }

  createEvent(groupId, eventData) {
    if (this.socket) {
      this.socket.emit('create_event', {
        group_id: groupId,
        event_data: eventData
      });
    }
  }

  castVote(pollId, optionId, userId) {
    if (this.socket) {
      this.socket.emit('cast_vote', {
        poll_id: pollId,
        option_id: optionId,
        user_id: userId
      });
    }
  }

  sendMessage(groupId, message) {
    if (this.socket) {
      this.socket.emit('send_message', {
        group_id: groupId,
        message: message
      });
    }
  }

  onEvent(event, callback) {
    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  offEvent(event, callback) {
    if (this.socket) {
      this.socket.off(event, callback);
    }
  }
}

export default new SocketService();
