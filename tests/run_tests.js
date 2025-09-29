const DimensionsTest = require('./test_dimensions.js');
const RoomCalculatorTest = require('./test_room_calculator.js');
const ValidationTest = require('./test_validation.js');
const InputValidationTest = require('./test_input_validation.js');
const RecommendationsTest = require('./test_recommendations.js');

class TestRunner {
    constructor() {
        this.tests = [
            new DimensionsTest(),
            new RoomCalculatorTest(),
            new ValidationTest(),
            new InputValidationTest(),
            new RecommendationsTest()
        ];
    }

    async runAll() {
        console.log('Starting Test Suite...\n');
        
        for (const test of this.tests) {
            console.log(`Running ${test.constructor.name}...`);
            await test.runTests();
            console.log('');
        }
        
        console.log('Test Suite Complete');
    }
}

// Run tests when file is executed directly
if (require.main === module) {
    const runner = new TestRunner();
    runner.runAll();
} 