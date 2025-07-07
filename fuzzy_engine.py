import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class DigitalMaturityAnalyzer:
    def __init__(self, template_path='templates/minobr_2025.json'):
        self.load_template(template_path)
        self.setup_fuzzy_system()

    def load_template(self, path):
        with open(path) as f:
            self.template = json.load(f)

        # Инициализация факторов
        self.technical = ctrl.Antecedent(np.arange(0, 4, 0.1), 'technical')
        self.cognitive = ctrl.Antecedent(np.arange(0, 4, 0.1), 'cognitive')
        self.personal = ctrl.Antecedent(np.arange(0, 4, 0.1), 'personal')
        self.maturity = ctrl.Consequent(np.arange(0, 100, 1), 'maturity')

        # Автоконфигурация из шаблона
        self.configure_functions()

    def configure_functions(self):
        # Автоматическое создание функций принадлежности
        for factor in [self.technical, self.cognitive, self.personal]:
            factor.automf(names=['low', 'medium', 'high'])

        self.maturity['level1'] = fuzz.trimf(self.maturity.universe, [0, 0, 40])
        self.maturity['level2'] = fuzz.trimf(self.maturity.universe, [30, 50, 70])
        self.maturity['level3'] = fuzz.trimf(self.maturity.universe, [60, 80, 100])

        # Загрузка правил из шаблона
        self.rules = []
        for rule in self.template['rules']:
            self.rules.append(ctrl.Rule(
                eval(rule['condition']),
                self.maturity[rule['result']]
            ))

        self.system = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(self.system)

    def assess(self, metrics):
        """Оценка цифровой зрелости"""
        self.simulator.input['technical'] = metrics['technical']
        self.simulator.input['cognitive'] = metrics['cognitive']
        self.simulator.input['personal'] = metrics['personal']

        self.simulator.compute()
        return self.simulator.output['maturity']

    def generate_roadmap(self, metrics):
        """Генерация дорожной карты"""
        maturity_level = self.assess(metrics)
        actions = []

        # Критические разрывы
        if metrics['technical'] - metrics['cognitive'] > 1.5:
            actions.append("Обучение цифровым компетенциям сотрудников")

        if metrics['data_security'] < 1.5:
            actions.append("Внедрение SIEM-системы")

        # Расчет ROI
        roi = self.calculate_roi(actions)

        return {
            "maturity_score": round(maturity_level, 2),
            "critical_gaps": self.identify_gaps(metrics),
            "priority_actions": actions,
            "estimated_roi": roi,
            "timeline": "6 месяцев"
        }

    def calculate_roi(self, actions):
        # Упрощенная модель расчета ROI
        return sum(len(action) * 15000 for action in actions)  # Примерная логика