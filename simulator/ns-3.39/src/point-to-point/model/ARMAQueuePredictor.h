// // ARMAQueuePredictor.h
// #pragma once
// #include <deque>
// #include <vector>

// class ARMAQueuePredictor {
// public:
//     ARMAQueuePredictor(int p, int q)
//         : p_(p), q_(q), phi_(p, 0.0), theta_(q, 0.0), history_(p, 0), error_(q, 0) {}

//     void Update(double newQueueLength) {
//         history_.push_back(newQueueLength);
//         if (history_.size() > p_) history_.pop_front();

//         double prediction = 0.0;
//         for (int i = 0; i < p_; ++i) {
//             prediction += phi_[i] * history_[history_.size() - 1 - i];
//         }
//         for (int j = 0; j < q_; ++j) {
//             prediction += theta_[j] * error_[error_.size() - 1 - j];
//         }

//         double error = newQueueLength - prediction;
//         error_.push_back(error);
//         if (error_.size() > q_) error_.pop_front();
//     }

//     double Predict() const {
//         double prediction = 0.0;
//         for (int i = 0; i < p_; ++i) {
//             prediction += phi_[i] * history_[history_.size() - 1 - i];
//         }
//         for (int j = 0; j < q_; ++j) {
//             prediction += theta_[j] * error_[error_.size() - 1 - j];
//         }
//         return prediction;
//     }
//     ARMAQueuePredictor(int p, int q) : p_(p), q_(q) {}
//     ARMAQueuePredictor() : p_(0), q_(0) {}  // 默认构造函数，初始化为默认值
// private:
//     int p_;  // AR 阶数
//     int q_;  // MA 阶数
//     std::vector<double> phi_;   // AR 系数
//     std::vector<double> theta_; // MA 系数
//     std::deque<double> history_; // 队列历史数据
//     std::deque<double> error_;   // 预测误差
// };
